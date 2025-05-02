# main.py
import sys
import math
import re
import sys
import math
import re
import sys
import math
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import (
    QCheckBox, QDialog, QVBoxLayout, QDialogButtonBox,
    QApplication, QMainWindow, QFileDialog, QMessageBox, QInputDialog,
    QPushButton, QHBoxLayout, QWidget, QLabel, QListWidgetItem, QTextEdit
)
from PySide6.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QEvent, QTimer, QProcess, QObject, Signal, QThread

from ui_interface import Ui_MainWindow
import fitz
from docx import Document
import textwrap
from docx.shared import Inches, Pt  # Add these imports for Word formatting
from database import (
    init_db, save_meeting, get_all_recordings,
    get_meeting_by_id, delete_meeting_by_id
)
from pathlib import Path
from os import makedirs,remove
from os.path import basename, dirname, join, abspath, exists
import re
from html.parser import HTMLParser


from minutes_extractor import MeetingMinutesExtractor, ModelConfig

class MinutesGeneratorWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)
    progress = Signal(int)  # Optional: for progress updates

    def __init__(self, transcript, agenda_items):
        super().__init__()
        self.transcript = transcript
        self.agenda_items = agenda_items
        self._is_running = True
        

    def run(self):
        try:
            # Initialize model configuration
            model_config = ModelConfig(
                model_name="yissus/llama-3.1-8b-q4:latest",
                temperature=0.5,
                mirostat=2.0
            )
            
            # Create extractor
            extractor = MeetingMinutesExtractor(
                model_config=model_config,
                output_language='English',
                max_workers=None
            )

            # Process in chunks (optional progress reporting)
            if not self._is_running:
                return

            # Get structured meeting minutes data
            meeting_data = extractor.extract_meeting_minutes(
                transcript=self.transcript,
                agenda=self.agenda_items
            )

            if not self._is_running:
                return

            self.finished.emit(meeting_data)
            
        except Exception as e:
            self.error.emit(f"Error generating minutes: {str(e)}")

    def cancel(self):
        self._is_running = False
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize QProcess
        self.transcription_process = None
        self.translation_process = None

        # State variables
        self.drawer_open = True
        self.is_maximized = False
        self.attendees = []
        self.agendas = []            
        self.speaker_map = {}
        self.current_meeting_id = None
        self.current_draft_id = None
        self.current_log_title = None
        self.current_log_agenda = None
        
        #Holder for transcript, minutes, translation whether for getting, saving, update
        self.title = ""
        self.meeting_id = None
        self.transcript = ""
        self.previous_transcript = ""
        self.minutes = ""
        self.is_translated = False
        self.translated_transcript = ""

        if hasattr(sys, '_MEIPASS'):
            self.script_dir = sys._MEIPASS
        else:
            self.script_dir = Path(__file__).parent
        
        # Connect the watcher
        self.ui.logTranscriptDisplay.textChanged.connect(self.watcher_function)
        
        self._set_page(self.ui.HomePage)
        self.raw_transcript_text = ""  # Stores actual conversation text
        self.transcript_html_template = ""  # Stores base HTML structure

        # Initialize UI & DB
        self._init_window()
        self._connect_signals()
        init_db()
        self._load_saved_recordings()
        self.show()

        # Initial button states
        self.ui.proceedBtn.setEnabled(False)
        self.ui.saveBtn.setEnabled(False)
        self._update_button_states()  # New initial state update
        self.ui.transcribeBtn.setEnabled(False)
        self.ui.saveBtn.setEnabled(False)
        self.ui.logSaveBtn.setEnabled(True)


        # Initialize threading and worker for minutes generation
        self.minutes_thread = None
        self.minutes_worker = None
        self.current_context = None  # For storing UI context during processing

        
  
    def _init_window(self):
        self.setFixedSize(1000, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.sideMenuContainer.setMinimumWidth(200)
        self.ui.sideMenuContainer.setMaximumWidth(200)
        
        # Set tooltip for the clear button
        self.ui.clearBtn.setToolTip("Clear Inputs")

        # Always show these controls
        self.ui.assignSpeakerBtn.setVisible(True)
        self.ui.replaceTextBtn.setVisible(True)
        self.ui.speakerNumber.setVisible(True)
        self.ui.speakerName.setVisible(True)
        
        # Initially disable inputs
        self.ui.speakerNumber.setEnabled(False)
        self.ui.speakerName.setEnabled(False)
        self.ui.assignSpeakerBtn.setEnabled(False)

    def _connect_signals(self):
        u = self.ui
        # Navigation
        u.homeButton.clicked.connect(lambda: self._set_page(u.HomePage))
        u.returnBtn.clicked.connect(lambda: self._set_page(u.GeneratePage1))
        u.LogButton.clicked.connect(lambda: self._set_page(u.activityListPage))
        u.returnLogBtn.clicked.connect(lambda: self._set_page(u.activityListPage))
        u.getStartedBtn.clicked.connect(lambda: self._set_page(u.GeneratePage1))
        u.clearBtn.clicked.connect(self._clear_and_go_home)
        u.logSaveBtn.clicked.connect(self._save_log_to_database)
        # File & export
        u.uploadBtn.clicked.connect(self._open_file_manager)
        u.proceedBtn.clicked.connect(self._translate)

        # Transcription and generation buttons
        u.transcribeBtn.clicked.connect(self._transcribe_audio)
        u.generateBtn.clicked.connect(self._generate_minutes)
        u.logGenerateBtn.clicked.connect(self._generate_log_minutes)
        # Window controls
        u.close.clicked.connect(self.close)
        u.minimizeWindow.clicked.connect(self.showMinimized)
        u.maximizeWindow.clicked.connect(self._toggle_maximize)
        u.sideDrawerButton.clicked.connect(self._toggle_drawer)
        # Text inputs
        u.attendeesInput.installEventFilter(self)
        u.agendaInput.installEventFilter(self)
        u.assignSpeakerBtn.clicked.connect(self._assign_speaker_name)
        u.replaceTextBtn.clicked.connect(self._replace_in_minutes)
        u.attendeesInput.textChanged.connect(self._update_attendees_list)
        u.agendaInput.textChanged.connect(self._update_agendas_list)
        # Database ops
        u.saveBtn.clicked.connect(self._save_to_database)
        u.savedListWidget.itemClicked.connect(self._load_selected_log)
        u.transcriptDisplay.textChanged.connect(self._update_button_states)
        u.minutesDisplay.textChanged.connect(self._update_button_states)

    # Connect the watcher
    def watcher_function(self):
        # Get the current text inside transcriptDisplay
        self.current_text = self.ui.logTranscriptDisplay.toPlainText()
        
    def _update_attendees_list(self):
        """Update attendees list from comma-separated input"""
        raw_text = self.ui.attendeesInput.toPlainText().strip()
        self.attendees = [name.strip() for name in raw_text.split(',') if name.strip()]
        self._update_transcript()

    def _update_agendas_list(self):
        """Update agenda list from comma-separated input"""
        raw_text = self.ui.agendaInput.toPlainText().strip()
        self.agendas = [agenda.strip() for agenda in raw_text.split(',') if agenda.strip()]
        self._update_transcript()

    def _transcribe_audio(self):
            #ITO SAYO JOE, SAMPLE LANG TO
    
            folders_outputs = "outputs"
            makedirs(folders_outputs, exist_ok=True)
            outputs_file_path = join(self.script_dir, folders_outputs, self.ui.uploadedFileLabel.text() + ".txt")

            if exists(outputs_file_path):
                remove(outputs_file_path)
            
            self.ui.transcribeBtn.setEnabled(False)
            self.ui.uploadBtn.setEnabled(False)
            
            self.file_path = self.path
            
            if not self.file_path:
                QMessageBox.warning(self, "Error", "Please upload an audio file first.")
                return
            
            # Store current scroll position, KEEP THIS DONT DELETE PLS! THANK YOU!
            scroll = self.ui.transcriptDisplay.verticalScrollBar().value()
            
            self.ui.transcriptDisplay.setPlainText("Transcribing... Please wait.")
            
            print("Model Accessed")

            min_speakers = "2"  # QProcess only accepts string arguments

            if self.transcription_process and self.transcription_process.state() == QProcess.Running:
                self.transcription_process.terminate()

            self.transcription_process = QProcess(self)

            # Get the absolute path of DiarizedTranscription.py inside "EZ"
            diarized_script_path = self.script_dir / "DiarizedTranscription.py"
            print("File Path Audio:", self.file_path)
            # Pass parameters properly as command-line arguments
            self.transcription_process.setArguments([
                str(diarized_script_path),
                self.file_path, min_speakers
            ])

            self.transcription_process.setProgram(sys.executable)  # Run with the same Python interpreter
            
            # self.transcription_process.readyReadStandardError.connect(self.read_error)
            self.transcription_process.readyReadStandardOutput.connect(self.read_output)
            
            # Connect signals
            self.transcription_process.finished.connect(lambda: self._complete_transcription(scroll))
        

            self.transcription_process.start()
            QApplication.processEvents()
    
    #ITO NAKA FORMA NA, STORE MO SA transcript VARIABLE MAGIGING OUTCOME NG TRANSCRIPTION
    def _complete_transcription(self, original_scroll):
        transcript = self.on_diarization_complete()
        print("transcript from transcribe model: " + transcript)
        current_time = datetime.now().strftime("%B %d, %Y | %I:%M %p")
        agenda_str = self._format_agendas()
        attendees_str = self._format_attendees(self.attendees)
        
        # Store raw transcript and template separately
        self.raw_transcript_text = transcript
        self.transcript_html_template = f"""
        <b>Meeting Date:</b> {current_time}<br><br>
        <b>Meeting Agenda:</b><br><pre>{{AGENDA}}</pre><br><br>
        <b>Meeting Attendees:</b><br><pre>{{ATTENDEES}}</pre><br>
        <b>Meeting Transcript:</b><br><pre>{{TRANSCRIPT}}</pre>
        """
        
        # Initial render
        html = self.transcript_html_template.format(
            AGENDA=agenda_str,
            ATTENDEES=(attendees_str),
            TRANSCRIPT=self.pre_wrap(self.raw_transcript_text)
        )
        self.ui.transcriptDisplay.setHtml(html)
        self.ui.transcriptDisplay.verticalScrollBar().setValue(original_scroll)
        self._update_button_states()
        
    def _update_button_states(self):
        #Updates Buttons and Condition, PLEASE KEEP!
        has_transcript = bool(self.ui.transcriptDisplay.toPlainText().strip())
        has_minutes = bool(self.ui.minutesDisplay.toPlainText().strip())
    
    # Enable speaker controls only if transcript exists. PLEASE KEEP!
        self.ui.speakerNumber.setEnabled(has_transcript)
        self.ui.speakerName.setEnabled(has_transcript)
        self.ui.assignSpeakerBtn.setEnabled(has_transcript)
        
        # Show/hide other buttons. PLEASE KEEP!
        self.ui.replaceTextBtn.setVisible(has_minutes)
    
    def highlight_text(self, file_content):
         # Regular expression to match words inside parentheses
            parentheses_pattern = r"\((.*?)\)"

            # Regular expression to match speaker lines: [time] SPEAKER X:
            # speaker_pattern = r"(\[\d+\.\d+\s*-\s*\d+\.\d+\]\s*SPEAKER\s*\d+:)"
            speaker_pattern = r"(\[\d+(\.\d+)?\s*-\s*\d+(\.\d+)?\]\s*.*?:)"

            # Replace words inside parentheses with red-colored text (without parentheses)
            formatted_text = re.sub(parentheses_pattern, r'<span style="color:red; font-weight:bold">\1</span>', file_content)

            # Replace speaker lines with green-colored text
            formatted_text = re.sub(speaker_pattern, r'<span style="color:green; font-weight:bold">\1</span>', formatted_text)

            # Preserve newlines by replacing '\n' with '<br>'
            formatted_text = formatted_text.replace("\n", "<br>")
            
            return formatted_text
        
    def highlight_texts(self, file_content):
        # Regular expression to match words inside parentheses
            parentheses_pattern = r"\((.*?)\)"

            # Regular expression to match speaker lines: [time] SPEAKER X:
            # speaker_pattern = r"(\[\d+\.\d+\s*-\s*\d+\.\d+\]\s*SPEAKER\s*\d+:)"
            speaker_pattern = r"(\[\d+(\.\d+)?\s*-\s*\d+(\.\d+)?\]\s*.*?:)"

            
            # Replace speaker lines with green-colored text
            formatted_text = re.sub(speaker_pattern, r'<span style="color:green; font-weight:bold">\1</span>', file_content)

            
            return formatted_text
        
    def on_diarization_complete(self):
        # Try to read the generated transcript file
        try:
            # script_directory = dirname(abspath(__file__))
            # parent_directory = dirname(script_directory)
            result_file_path = join(self.script_dir, 'outputs', basename(self.file_path) + ".txt")
            if not exists(result_file_path):
                print("Transcript file not found")
                self._transcribe_audio()
                return
            else:
                with open(result_file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()  # Read the entire file content

            formatted_text  = self.highlight_text(file_content)  
            
            html_text = self.ui.transcriptDisplay.toHtml()
            match = re.search(r"(.*?Meeting Transcript:)", html_text, re.DOTALL)

            if match:
                header = match.group(1)
            else:
                header = "Meeting Transcript:"  # fallback/default if no match

            self.ui.transcriptDisplay.setHtml(header + "<br>" + formatted_text)
            
            self.ui.uploadBtn.setEnabled(True)
            self.ui.transcribeBtn.setEnabled(True)
            self.ui.proceedBtn.setEnabled(True)
            self.cleanup_transcription()
            
            return formatted_text

        except Exception as e:
            print(f"Error reading file: {e}")
            self.ui.uploadBtn.setEnabled(True)
            self.ui.transcribeBtn.setEnabled(True)
            self.ui.proceedBtn.setEnabled(True)
            return "None Transcripted"
    
    def read_translation_output(self):
        """Read process standard output and print to console"""
        output = self.translation_process.readAllStandardOutput().data().decode()
        print(output)
        
    def read_output(self):
        """Read process standard output and print to console"""
        output = self.transcription_process.readAllStandardOutput().data().decode()
    
        self.previous_transcript = self.ui.transcriptDisplay.toHtml().strip
        
    def _translate(self):
        print("translation processing")
        self.ui.transcribeBtn.setEnabled(False)
        self.ui.uploadBtn.setEnabled(False)
        self.ui.proceedBtn.setEnabled(False)
        
        if self.translation_process and self.translation_process.state() == QProcess.Running:
            self.translation_process.terminate()

        self.translation_process = QProcess(self)

        # Get the absolute path of translation.py inside "EZ"
        translation_script_path = self.script_dir / "translation.py"
        self.transcripted = self.ui.transcriptDisplay.toPlainText()
        
        print(self.transcripted)
            
        draft_title = f"Transcript Draft {datetime.now().strftime('%m/%d/%Y at %I:%M %p')}"
        agenda_text = "\n".join(self.agendas).strip()
        translated_transcript = ""
        minutes = ""
        self.file_name = self.ui.uploadedFileLabel.text()
        
        self.meeting_id = save_meeting(self.file_name,draft_title, agenda_text, self.transcripted, False, translated_transcript , minutes,
            is_draft=1, meeting_id=self.current_draft_id)
        
        print(self.meeting_id)
        
        # Pass parameters properly as command-line arguments
        self.translation_process.setArguments([
            str(translation_script_path),
            str(self.meeting_id),
            self.ui.uploadedFileLabel.text()
            
        ])

        self.translation_process.setProgram(sys.executable)  # Run with the same Python interpreter

        # Connect signals
        self.translation_process.finished.connect(self.complete_translation)

        self.translation_process.start()
        
            
    def complete_translation(self):
        """Read process standard output and print to console"""
        self.translated_transcript = self.translation_process.readAllStandardOutput().data().decode()
        
        print("self.trans:\n\n"+ self.translated_transcript)
        
        if not self.translated_transcript:
            self.translated_file_path = self.script_dir / "translations" / ("translated_" + basename(self.file_path) + ".txt")
            if self.translated_file_path:
                if exists(self.translated_file_path):
                    print("existing ang file")
                    self.translated_file_path = str(self.translated_file_path)  
                    
                    with open(self.translated_file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()  # Read the entire file content
                        
                    self.translated_transcript = file_content
                else:
                    print("File not found, run translate again")
                    self._translate()
            else:
                print("no file path, run translate again")
                self._translate()
        
        print("translated_transcript: "+ self.translated_transcript)
        print("transcription successfully translated")
        self.is_translated = True
        self.ui.transcribeBtn.setEnabled(True)
        self.ui.uploadBtn.setEnabled(True)
        self.ui.proceedBtn.setEnabled(True)
        self.cleanup_translation()
        self._save_transcript_and_proceed()
        
            
    def complete_log_translation(self):
        """Read process standard output and print to console"""
        self.translated_transcript = self.translation_process.readAllStandardOutput().data().decode()
        
        if not self.translated_transcript:
            self.translated_file_path = self.script_dir / "translations" / ("translated_" + basename(self.title) + ".txt")
            if self.translated_file_path:
                if exists(self.translated_file_path):
                    print("existing ang file")
                    self.translated_file_path = str(self.translated_file_path)   
                    
                    with open(self.translated_file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()  # Read the entire file content
                        
                    self.translated_transcript = file_content
                else:
                    print("File not found, run translate again")
                    self._translate()
            else:
                print("no file path, run translate again")
                self._translate()
        
        print("translated_transcript: " + self.translated_transcript)
        
        print("log transcription successfully translated")
        self.is_translated = True
        self.ui.logMinutesDisplay.setPlainText("Generating minutes... Please wait.")
        print("translated transcript top from logs: "+self.translated_transcript)
        self.cleanup_translation()
        
        self.translate_call_generate_minutes_from_transcript(self.translated_transcript)

    # ======== MINUTES GENERATION METHODS ========
    
    def _generate_minutes(self):
        self.ui.homeButton.setEnabled(False)
        self.ui.LogButton.setEnabled(False)
        
        print("self is translated: ", self.is_translated)
        
        print("Transcript TRANSLATED"+ self.translated_transcript)
        """Generate meeting minutes from the transcript display"""
        if self.translated_transcript:
            transcript = self.translated_transcript
        else:
            transcript = self.ui.transcriptDisplay.toPlainText()
            
        print("Transcript to be passed: "+ transcript)

        
        if not transcript:
            QMessageBox.warning(self, "Error", "No transcript available. Please transcribe an audio file first.")
            return
        
        self.ui.minutesDisplay.setPlainText("Generating minutes... Please wait.")
        QApplication.processEvents()
        
        # Get UI components for main minutes display
        ui_components = {
            'output_display': self.ui.minutesDisplay,
            'attendees_list': self.attendees,
            'agenda_items_list': self.agendas,
            'success_title': "Minutes Generated",
            'success_message': "Meeting minutes have been generated successfully."
        }
        
        # This will now use the threaded version
        self._generate_minutes_from_transcript(transcript, ui_components)

    def _generate_log_minutes(self):
        """Generate minutes from a loaded log transcript"""
        #For converting from html to plaintext
        self.ui.minutesDisplay.setHtml(self.transcript)
        transcript_compare = self.ui.minutesDisplay.toPlainText()
        transcript_compare = transcript_compare
        self.ui.minutesDisplay.setPlainText("")
        
        if self.is_translated and self.translated_transcript:
            if transcript_compare.strip() == self.current_text.strip():
                if self.minutes:
                    print("same sila and existing minutes")
                    transcript = self.translated_transcript
                    self.translate_call_generate_minutes_from_transcript(transcript)
                else:
                    print("same sila but no existing minutes")
                    transcript = self.translated_transcript
                    self.translate_call_generate_minutes_from_transcript(transcript)
            else:
                print("di sila same need log_translate, pero need rin iangat yung calling ng model ni alex")
                transcript = self.current_text.strip()
                self.translate_call_generate_minutes_from_transcript(transcript)
                # self._log_translate()

        else:
            print("di same, and false yung self.is_translated and wala laman self.translated_transcript")
            print("need log_translate, pero need rin iangat yung calling ng model ni alex")
            transcript = self.current_text.strip()
            self.translate_call_generate_minutes_from_transcript(transcript)
            # self._log_translate()
            
        # print("pinasang transcript for minutes generation: \n" + transcript)
            
        # print(self.is_translated)
        
        
    def translate_call_generate_minutes_from_transcript(self, transcript):
        if not transcript:
            QMessageBox.warning(self, "Error", "No transcript available in the log.")
            return
            
        # self.ui.logMinutesDisplay.setPlainText("Generating minutes... Please wait.")
        QApplication.processEvents()
        
        print("eto na talag ayung bago ipasa sa minutes generation: "+ transcript)
        
        # Get UI components for log minutes display
        ui_components = {
            'output_display': self.ui.logMinutesDisplay,
            'attendees_list': [], # Empty attendees list for log minutes (we'll extract from transcript)
            'agenda_items_list': [], # Empty agendas list for log minutes (we'll extract from transcript)
            'success_title': "Minutes Generated",
            'success_message': "Meeting minutes have been generated from the log transcript."
        }
        
        QTimer.singleShot(1500, lambda: self._generate_minutes_from_transcript(transcript, ui_components))


    def _generate_minutes_from_transcript(self, transcript_text, ui_components):
        print("eto nasa loob ng ng minutes generation: \n\n\n"+ transcript_text)

        """Shared method to generate minutes from transcript text
        
        Args:
            transcript_text: The transcript text to process
            ui_components: Dictionary containing UI-specific components and settings
                - output_display: The text display to update with minutes
                - attendees_list: List of attendees (if available)
                - agenda_items_list: List of agenda items (if available)
                - success_title: Title for success message
                - success_message: Content for success message
        """
        # Extract components
        output_display = ui_components['output_display']
        attendees_list = ui_components['attendees_list']
        agenda_items_list = ui_components['agenda_items_list']
        success_title = ui_components['success_title']
        success_message = ui_components['success_message']
        
        # Extract sections by keys
        sections = self._extract_sections(transcript_text)
        
        # Get individual sections
        date_line = sections.get("Meeting Date", "")
        agenda_text = sections.get("Meeting Agenda", "")
        attendees_text = sections.get("Meeting Attendees", "")
        transcript = sections.get("Meeting Transcript", "").strip()
        
        # # Use provided agenda items if available, otherwise parse from transcript
        # final_agenda_items = agenda_items_list.copy()
        final_agenda_items= []
        # If agenda items aren't provided, try to parse from transcript
        if agenda_text and "No data input" not in agenda_text:
            for line in agenda_text.split('\n'):
                line = line.strip()
                if line and line.startswith('•'):
                    final_agenda_items.append(line[1:].strip())

        # Use provided attendees if available, otherwise fallback to transcript text
        if attendees_list:
            final_attendees = attendees_list
        elif "No data input" not in attendees_text:
            final_attendees = []
            for line in attendees_text.splitlines():
                line = line.strip()
                if not line:
                    continue
                # Split by large spaces (separate names first)
                names = re.split(r'\s{2,}', line)
                for name in names:
                    name = name.strip()
                    if not name:
                        continue
                    # Now remove numbering like "1. Name", "3. Name", etc for each name
                    clean_name = re.sub(r'^\d+\.\s*', '', name)
                    final_attendees.append(clean_name)
        else:
            final_attendees = ["No attendees recorded"]

        final_attendees = self._format_attendees(final_attendees, cols=3)


 
        # Store context for when processing completes
        self.current_context = {
            'output_display': ui_components['output_display'],
            'date_line': date_line,
            'final_attendees': final_attendees,
            'final_agenda_items': final_agenda_items,
            'success_title': ui_components['success_title'],
            'success_message': ui_components['success_message']
        }

        # Create thread and worker
        self.minutes_thread = QThread()
        self.minutes_worker = MinutesGeneratorWorker(transcript, final_agenda_items)
        
        # Move worker to thread
        self.minutes_worker.moveToThread(self.minutes_thread)
        
        # Connect signals
        self.minutes_thread.started.connect(self.minutes_worker.run)
        self.minutes_worker.finished.connect(self._handle_minutes_success)
        self.minutes_worker.error.connect(self._handle_minutes_error)
        self.minutes_worker.finished.connect(self.minutes_thread.quit)
        self.minutes_worker.error.connect(self.minutes_thread.quit)
        self.minutes_thread.finished.connect(self._cleanup_thread)
        
        self.ui.minutesDisplay.setEnabled(True)
        self.ui.logMinutesDisplay.setEnabled(True)


        # Show processing message
        ui_components['output_display'].setPlainText("Generating minutes... Please wait.")
        
        # Start the thread
        self.minutes_thread.start()

    def _handle_minutes_success(self, meeting_data):
        """Handle successful minutes generation"""
        if not self.current_context:
            return

        # Build the minutes HTML
        minutes = self._build_minutes_html(
            date_line=self.current_context['date_line'],
            attendees=self.current_context['final_attendees'],
            meeting_data=meeting_data,
            agenda_items=self.current_context['final_agenda_items']
        )
        
        # Update UI
        self.current_context['output_display'].setHtml(minutes)
        QMessageBox.information(
            self,
            self.current_context['success_title'],
            self.current_context['success_message']
        )
        
        self._cleanup_context()

    def _handle_minutes_error(self, error_msg):
        """Handle errors during minutes generation"""
        QMessageBox.critical(self, "Generation Error", error_msg)
        self._cleanup_context()

    def _cleanup_thread(self):
        """Clean up thread resources"""
        if self.minutes_thread:
            self.minutes_thread.quit()
            self.minutes_thread.wait()
            self.minutes_thread.deleteLater()
            self.minutes_thread = None
        
        if self.minutes_worker:
            self.minutes_worker.deleteLater()
            self.minutes_worker = None
        
        self.ui.returnBtn.setEnabled(True)
        self.ui.generateBtn.setEnabled(True)
        self.ui.saveBtn.setEnabled(True)
        self.ui.returnLogBtn.setEnabled(True)
        self.ui.logGenerateBtn.setEnabled(True)
        self.ui.logSaveBtn.setEnabled(True)
        self.ui.homeButton.setEnabled(True)
        self.ui.LogButton.setEnabled(True)
        
    def cleanup_translation(self):
        # Cleanup in the main process (QProcess)
        if self.translation_process.state() == QProcess.Running:
            print("Terminating process...")
            self.translation_process.terminate()

        if self.translation_process.state() == QProcess.Running:
            print("Forcing kill...")
            self.translation_process.kill()
            
        # Disconnect any signal-slot connections (if applicable)
        try:
            self.translation_process.finished.disconnect()
            print("Disconnected finished signal.")
        except Exception as e:
            print(f"Error disconnecting signal: {e}")


        self.translation_process.waitForFinished()
        del self.translation_process
        self.translation_process = None
        print("Main process cleaned up. and reinitialized")
        
    def cleanup_transcription(self):
        # Cleanup in the main process (QProcess)
        if self.transcription_process.state() == QProcess.Running:
            print("Terminating process...")
            self.transcription_process.terminate()

        if self.transcription_process.state() == QProcess.Running:
            print("Forcing kill...")
            self.transcription_process.kill()
            
        # Disconnect any signal-slot connections (if applicable)
        try:
            self.transcription_process.finished.disconnect()
            print("Disconnected finished signal.")
        except Exception as e:
            print(f"Error disconnecting signal: {e}")

        self.transcription_process.waitForFinished()
        del self.transcription_process
        self.transcription_process = None
        print("Main process cleaned up. and reinitialized")
        
    def _cleanup_context(self):
        """Clean up context resources"""
        if hasattr(self, 'current_context'):
            del self.current_context

    def closeEvent(self, event):
        """Ensure threads are cleaned up when window closes"""
        if self.minutes_thread and self.minutes_thread.isRunning():
            self.minutes_worker.cancel()
            self.minutes_thread.quit()
            self.minutes_thread.wait()
        
        super().closeEvent(event)

    def pre_wrap(self, text):
        return f'<pre style="white-space: pre-wrap;">{text.strip()}</pre>'
    
    def _build_minutes_html(self, date_line, attendees, meeting_data, agenda_items):
        """Build HTML content for meeting minutes"""
        
        
        minutes = f""" 
        <b>MINUTES OF THE MEETING</b> <br> 
        <b>Meeting Date: {date_line}</b> <br><br>
        
        <b>ATTENDEES:</b><br>
        {self.pre_wrap(attendees)}
        
        <b>MEETING AGENDA:</b> 
        """
        
        # Use agenda items from the extractor result if available, otherwise use parsed items
        if "agenda_items" in meeting_data and meeting_data["agenda_items"]:
            agenda_text = self._format_agenda_items_from_extractor(meeting_data["agenda_items"])
            minutes += self.pre_wrap(agenda_text)
        elif agenda_items:
            agenda_text = self._format_list_items(agenda_items)
            minutes += self.pre_wrap(agenda_text)
        else:
            minutes += self.pre_wrap("No agenda items recorded")
        
        # Add the rest of the minutes
        minutes += f"""
        <br><b>MEETING OVERVIEW:</b><br> 
        {self.pre_wrap(meeting_data["meeting_overview"])}<br><br>
        
        <br><b>DISCUSSION POINTS:</b>
        {self.pre_wrap(self._format_discussion_points(meeting_data["discussion_points"]))}
        
        <br><b>ACTION ITEMS:</b>
        {self.pre_wrap(self._format_action_items(meeting_data["action_items"]))}
        """
        
        return minutes

    # ======== FORMATTING METHODS ========
    def _extract_sections(self, text):
        """Extract sections from text based on key headers"""
        sections = {}
        
        # Define the keys we're looking for
        keys = [
            "Meeting Date",
            "Meeting Agenda",
            "Meeting Attendees",
            "Meeting Transcript"
        ]
        
        # Find each key and its content
        for i, key in enumerate(keys):
            start_pos = text.find(key + ":")
            
            if start_pos != -1:
                # Move past the key
                start_pos += len(key) + 1
                
                # Find the end (next key or end of text)
                end_pos = len(text)
                for next_key in keys:
                    next_pos = text.find(next_key + ":", start_pos)
                    if next_pos != -1 and next_pos < end_pos:
                        end_pos = next_pos
                
                # Extract the content
                content = text[start_pos:end_pos].strip()
                sections[key] = content
        
        return sections

    def _format_list(self, items, prefix="", empty_message="No items recorded"):
        """Generic formatter for lists with customizable prefix and empty message"""
        if not items:
            return empty_message
        
        formatted = []
        for i, item in enumerate(items):
            if prefix:
                formatted.append(f"{prefix}{item}")
            else:
                formatted.append(f"{i+1}. {item}")
        
        return "\n".join(formatted)

    def _format_dict_items(self, items, empty_message="No items recorded", 
                       key_field='title', prefix_type='number'):
        """Format dictionary items with flexible key field and prefix type"""
        if not items:
            return empty_message
        
        formatted_items = ""
        for i, item in enumerate(items):
            if isinstance(item, dict) and key_field in item:
                prefix = f"{i+1}. " if prefix_type == 'number' else "• "
                formatted_items += f"{prefix}{item[key_field]}\n"
            elif isinstance(item, str):
                prefix = f"{i+1}. " if prefix_type == 'number' else "• "
                formatted_items += f"{prefix}{item}\n"
            else:
                prefix = f"{i+1}. " if prefix_type == 'number' else "• "
                formatted_items += f"{prefix}{str(item)}\n"
        
        return formatted_items

    def _format_agenda_items_from_extractor(self, agenda_items):
        """Format agenda items returned from the extractor"""
        return self._format_dict_items(agenda_items, 
                                  empty_message="No agenda items recorded",
                                  key_field='title', 
                                  prefix_type='number')

    def _format_list_items(self, items):
        """Format a list of items with numbers"""
        return self._format_list(items, prefix="", empty_message="No items recorded")

    def _format_discussion_points(self, discussion_points):
        """Format discussion points with nested structure"""
        if not discussion_points:
            return "No discussion points recorded"
        
        formatted_points = ""
        for i, point_group in enumerate(discussion_points):
            # Handle if agenda_item exists
            if isinstance(point_group, dict) and 'agenda_item' in point_group:
                formatted_points += f"{i+1}. {point_group['agenda_item']}:\n"
                
                # Format individual points
                if 'points' in point_group:
                    for j, point_data in enumerate(point_group['points']):
                        if isinstance(point_data, dict) and 'point' in point_data:
                            # Include speaker if available
                            if 'speaker' in point_data:
                                formatted_points += f"   - {point_data['speaker']}: {point_data['point']}\n"
                            else:
                                formatted_points += f"   - {point_data['point']}\n"
                        else:
                            formatted_points += f"   - {point_data}\n"
                formatted_points += "\n"
            else:
                # Handle simple string points
                formatted_points += f"{i+1}. {point_group}\n"
        
        return formatted_points

    def _format_action_items(self, action_items):
        """Format action items with assignees if available"""
        if not action_items:
            return "No action items recorded"
        
        formatted_items = ""
        for i, item in enumerate(action_items):
            if isinstance(item, dict):
                # Format with assignee if available
                if 'assignee' in item and 'action' in item:
                    formatted_items += f"{i+1}. {item['assignee']}: {item['action']}\n"
                elif 'action' in item:
                    formatted_items += f"{i+1}. {item['action']}\n"
                else:
                    formatted_items += f"{i+1}. {str(item)}\n"
            else:
                formatted_items += f"{i+1}. {item}\n"
        
        return formatted_items

    def eventFilter(self, obj, event):
        # Handle Enter key for comma separation
        if (obj in (self.ui.attendeesInput, self.ui.agendaInput) and 
            event.type() == QEvent.KeyPress and 
            event.key() == Qt.Key_Return):
            
            cursor = obj.textCursor()
            cursor.insertText(", ")
            return True
            
        return super().eventFilter(obj, event)

    def _format_attendees(self, names, cols=3):
        if not names:
            return "No data input"
        rows = math.ceil(len(names) / cols)
        lines = []
        for r in range(rows):
            row = []
            for c in range(cols):
                i = r + c * rows
                if i < len(names):
                    row.append(f"{i+1:>3}. {names[i]:<25}")
            lines.append("".join(row).rstrip())
        return "\n".join(lines)

    def _format_agendas(self):
        if not self.agendas:
            return "No data input"
        return "\n".join([f"• {agenda}" for agenda in self.agendas])

    def _update_transcript(self):
        agenda_str = self._format_agendas()
        attendees_str = self._format_attendees(self.attendees)
        filename = self.ui.uploadedFileLabel.text()
        
        # Show filename if no transcript exists
        transcript_content = ""
        if not self.raw_transcript_text:
            if filename:
                transcript_content = f"[Uploaded File: {filename}]"
        else:
            transcript_content = self.raw_transcript_text
        
        # Rebuild HTML using template
        html = self.transcript_html_template.format(
            AGENDA=agenda_str,
            ATTENDEES=attendees_str,
            TRANSCRIPT=transcript_content
        )

        formatted_text  = self.highlight_texts(html)  
        self.ui.transcriptDisplay.setHtml(html)
        self._update_button_visibility()

    def _open_file_manager(self):
        print("open file manager")
        # Define filters for Audio, Video, and All Files
        audio_filter = "Audio Files (*.mp3 *.aac *.aiff *.flac *.m4a *.wav *.wma *.ogg *.mp2)"
        video_filter = "Video Files (*.mp4 *.mkv *.avi *.flv *.mov *.webm *.wmv *.mpeg *.mpg *.3gp)"
        all_filter = "All Files (*.*)"
        
        # Use QFileDialog with multiple filters and options
        self.path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "",
            f"{audio_filter};;{video_filter};;{all_filter}"  # Multiple filters separated by `;;
        )
        
        if self.path:
            self.ui.uploadedFileLabel.setText(self.path.split("/")[-1])
            self.ui.transcribeBtn.setEnabled(True)
            self.ui.proceedBtn.setEnabled(False)
            self.ui.saveBtn.setEnabled(False)

    def _wrap_text(self, text, width):
        wrapped = []
        for line in text.split('\n'):
            wrapped_lines = textwrap.wrap(line, width=width, break_long_words=True)
            wrapped.extend(wrapped_lines or [''])
        return wrapped

    def _save_pdf(self, file_path, sections):
        doc = fitz.open()
        w, h = 595, 842
        margin = 50
        line_height = 14

        for title, text in sections:
            page = doc.new_page(width=w, height=h)
            y = margin
            page.insert_text((margin, y), title,
                             fontsize=14, fontname="helv", render_mode=3)
            y += 2 * line_height
            
            wrapped_lines = self._wrap_text(text, 70)
            font_size = 9
            
            for line in wrapped_lines:
                if y + line_height > h - margin:
                    page = doc.new_page(width=w, height=h)
                    y = margin
                page.insert_text((margin, y), line,
                                 fontsize=font_size, fontname="courier")
                y += line_height
        doc.save(file_path)

    def _save_word(self, file_path, sections):
        doc = Document()
        for title, text in sections:
            p = doc.add_paragraph()
            r = p.add_run(title)
            r.bold = True
            wrapped_lines = self._wrap_text(text, 80)
            
            for line in wrapped_lines:
                if line.startswith(("Meeting Agenda", "Meeting Attendees")):
                    p = doc.add_paragraph()
                    r = p.add_run(line)
                    r.bold = True
                else:
                    doc.add_paragraph(line)
        doc.save(file_path)


    def _assign_speaker_name(self):
        # Get current scroll position
        scroll = self.ui.transcriptDisplay.verticalScrollBar().value()
        
        if not self.raw_transcript_text:  # Changed condition
            QMessageBox.warning(self, "Error", "Please transcribe an audio file first.")
            return

        speaker_number = self.ui.speakerNumber.toPlainText().strip()
        speaker_name = self.ui.speakerName.toPlainText().strip()
        
        # Validation
        if not speaker_number:
            QMessageBox.warning(self, "Missing Information", "Please enter a speaker number.")
            return
            
        if not speaker_name:
            QMessageBox.warning(self, "Missing Information", "Please enter a speaker name.")
            return
        
        # Normalize the speaker number input (remove "Speaker " prefix if present)
        if speaker_number.lower().startswith("speaker "):
            speaker_num = speaker_number[8:].strip()
        else:
            speaker_num = speaker_number.strip()
        
        # Create the standardized speaker tag to search for
        speaker_tag = f"SPEAKER {speaker_num}"
        
        original_text = self.raw_transcript_text  # Changed source
        
        # Use regular expression for case-insensitive replacement
        
        pattern = re.compile(re.escape(f"SPEAKER {speaker_num}"), re.IGNORECASE)
        new_text = pattern.sub(speaker_name, original_text)
        
        if original_text == new_text:
            QMessageBox.warning(self, "Not Found", 
                            f"Speaker tag 'SPEAKER {speaker_num}' not found in transcript.")
            return
            
        # Update both the stored raw text and display
        self.raw_transcript_text = new_text  # Store modified text
        self.speaker_map[speaker_tag] = speaker_name
        
        
        # Refresh display using the template
        self._update_transcript()  # This will rebuild the HTML
        
        # Restore scroll position
        self.ui.transcriptDisplay.verticalScrollBar().setValue(scroll)
        
        self.ui.speakerNumber.clear()
        self.ui.speakerName.clear()

    def _update_transcript_with_speaker_names(self):
        raw = self.ui.transcriptDisplay.toPlainText()
        for tag, name in self.speaker_map.items():
            raw = raw.replace(tag, name)
        self.ui.transcriptDisplay.setPlainText(raw)
        self._update_button_visibility()

    def _replace_in_minutes(self):
        find_txt, ok1 = QInputDialog.getText(
            self, "Find Text", "Enter text to find:"
        )
        if not ok1:
            return
        repl_txt, ok2 = QInputDialog.getText(
            self, "Find Text", "Enter text to replace with:"
        )
        if not ok2:
            return
        orig = self.ui.minutesDisplay.toPlainText()
        self.ui.minutesDisplay.setPlainText(orig.replace(find_txt, repl_txt))
        self._update_button_visibility()

    def _update_button_visibility(self):
        has_transcript = bool(self.ui.transcriptDisplay.toPlainText().strip())
        has_minutes    = bool(self.ui.minutesDisplay.toPlainText().strip())
        self.ui.assignSpeakerBtn.setVisible(has_transcript)
        self.ui.replaceTextBtn.setVisible(has_minutes)

    def _toggle_drawer(self):
        start = self.ui.sideMenuContainer.width()
        end = 0 if start > 0 else 200
        self.drawer_open = (end > 0)
        self._animate_drawer(start, end)

    def _animate_drawer(self, start_width, end_width):
        if getattr(self, "_drawer_anim", None) and self._drawer_anim.state():
            self._drawer_anim.stop()

        group = QParallelAnimationGroup(self)
        for prop in (b"minimumWidth", b"maximumWidth"):
            anim = QPropertyAnimation(self.ui.sideMenuContainer, prop)
            anim.setDuration(250)
            anim.setStartValue(start_width)
            anim.setEndValue(end_width)
            group.addAnimation(anim)
        group.start()
    def _clear_and_go_home(self):
        """
        Clear all inputs and content from GeneratePage1 and GeneratePage2 and navigate back to the HomePage
        """
        # Ask the user to confirm
        confirm = QMessageBox.question(
            self, "Confirm Clear",
            "Are you sure you want to clear all content and return to the home page?\n"
            "Any unsaved work will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Clear all inputs and content
            self._clear_all_content()
            
            # Navigate back to the home page
            self._set_page(self.ui.HomePage)
            
            # Show confirmation
            QMessageBox.information(self, "Cleared", "All inputs has been cleared successfully.")

    def _clear_all_content(self):
        """
        Clear all inputs and content from GeneratePage1 and GeneratePage2
        """
        # Clear file upload
        self.ui.uploadedFileLabel.setText("")
        
        # Clear attendees
        self.ui.attendeesInput.clear()
        self.attendees.clear()
        
        # Clear agenda items
        self.ui.agendaInput.clear()
        self.agendas.clear()
        
        # Clear transcript and minutes displays
        self.ui.transcriptDisplay.clear()
        self.ui.minutesDisplay.clear()
        self.raw_transcript_text = ""
        self.transcript_html_template = ""
        
        # Clear speaker inputs
        self.ui.speakerNumber.clear()
        self.ui.speakerName.clear()
        
        # Reset speaker mappings
        self.speaker_map.clear()
        
        # Reset meeting IDs
        self.current_meeting_id = None
        self.current_draft_id = None
        
        # Reset UI elements
        self._update_button_states()
        self._update_button_visibility()
        
        # Reset other displays if needed
        self.ui.logTranscriptDisplay.clear()
        self.ui.logMinutesDisplay.clear()
        
    def _toggle_maximize(self):
        if self.is_maximized:
            self.showNormal()
        else:
            self.showMaximized()
        self.is_maximized = not self.is_maximized

    def _save_transcript_and_proceed(self):
        raw_text = self.ui.transcriptDisplay.toPlainText()
        lines = raw_text.splitlines()
        
        content_lines = [
            line for line in lines 
            if line.strip() and 
            not line.startswith(("Meeting Date:", "Meeting Agenda:", "Meeting Attendees:", "Meeting Transcript:"))
        ]

        is_empty = (
            not self.agendas and 
            not self.attendees and 
            not any("•" in line for line in lines) and
            not any(line.strip().isdigit() for line in lines) and
            not content_lines
        )

        if is_empty:
            QMessageBox.warning(
                self,
                "Empty Draft",
                "Cannot save empty draft!\nPlease transcribe a recording or add meeting details first."
            )
            return

        draft_title = f"Transcript Draft {datetime.now().strftime('%m/%d/%Y at %I:%M %p')}"
        agenda_text = "\n".join(self.agendas).strip()
        transcript = self.ui.transcriptDisplay.toHtml().strip()
        is_translated = self.is_translated
        translated_transcript  = self.translated_transcript
        minutes = ""
        


        draft_id = save_meeting(
            self.file_name,draft_title, agenda_text, transcript, is_translated, translated_transcript , minutes,
            is_draft=1, meeting_id=self.meeting_id
        )
        
        print("is it same id? ", draft_id)
        if draft_id:
            self.current_draft_id = draft_id
            QMessageBox.information(self, "Saved", "Draft updated successfully.")
            self._load_saved_recordings()
            self.ui.proceedBtn.setEnabled(False)
            QTimer.singleShot(1000, lambda: self.ui.proceedBtn.setEnabled(True))
            self._set_page(self.ui.GeneratePage2)
        else:
            QMessageBox.warning(self, "Error", "Failed to save draft.")

    def _save_to_database(self):
            # Create export dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Click Ok to Save Record")
        layout = QVBoxLayout()
        
        # Create checkboxes
        transcript_cb = QCheckBox("Export Transcript")
        minutes_cb = QCheckBox("Export Minutes")
        
        # Create button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        # Add widgets to layout
        layout.addWidget(transcript_cb)
        layout.addWidget(minutes_cb)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        # Connect buttons
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        # Show dialog
        if dialog.exec() != QDialog.Accepted:
            return
        
        # Get user choices
        export_transcript = transcript_cb.isChecked()
        export_minutes = minutes_cb.isChecked()
        
        # Handle export
        sections = []
        text = self.ui.transcriptDisplay.toPlainText().strip()
        mins = self.ui.minutesDisplay.toPlainText().strip()
        
        if export_transcript and text:
            sections.append(("Meeting Transcript", text))
        if export_minutes and mins:
            sections.append(("Minutes of the Meeting", mins))
        
        if sections:
            path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", 
                "PDF Files (*.pdf);;Word Files (*.docx)"
            )
            if path:
                if path.endswith(".pdf"):
                    self._save_pdf(path, sections)
                elif path.endswith(".docx"):
                    self._save_word(path, sections)
                QMessageBox.information(self, "Exported", f"File saved to:\n{path}")

        # Always save to database
        raw_text = self.ui.transcriptDisplay.toHtml()
        mins_text = self.ui.minutesDisplay.toPlainText().strip()
        is_translated = self.is_translated
        translated_transcript  = self.translated_transcript
        
        is_empty = (
            not self.agendas and 
            not self.attendees and 
            not raw_text.strip() and 
            not mins_text
        )

        if is_empty:
            QMessageBox.warning(
                self,
                "Empty Meeting",
                "Cannot save empty meeting!\nPlease add content before saving."
            )
            return

        final_title = f"Recording {datetime.now().strftime('%m/%d/%Y at %I:%M %p')}"
        agenda_text = "\n".join(self.agendas).strip()
        transcript = raw_text.strip()
        minutes = mins_text

        final_id = save_meeting(self.file_name,final_title, agenda_text, transcript, is_translated, translated_transcript , minutes, is_draft=0)
        
        if final_id:
            if self.current_draft_id:
                delete_meeting_by_id(self.current_draft_id)
                self.current_draft_id = None

            QMessageBox.information(self, "Saved", "Record Saved successfully.")
            self.ui.saveBtn.setEnabled(False)
            QTimer.singleShot(1000, lambda: self.ui.saveBtn.setEnabled(True))
            self._load_saved_recordings()
            self._clear_generate_pages()
            self._set_page(self.ui.GeneratePage1)  # Navigate back to GeneratePage1
            
            is_empty = (
                not self.agendas and 
                not self.attendees and 
                not raw_text.strip() and 
                not mins_text
            )

            if is_empty:
                QMessageBox.warning(
                    self,
                    "Empty Meeting",
                    "Cannot save empty meeting!\nPlease add content before saving."
                )
                return

            # final_title = f"Record {datetime.now().strftime('%m/%d/%Y at %I:%M %p')}"
            # agenda_text = "\n".join(self.agendas).strip()
            # transcript = raw_text.strip()
            # minutes = mins_text

            # final_id = save_meeting(final_title, agenda_text, transcript, minutes, is_draft=0)
            
            # if final_id:
            #     if self.current_draft_id:
            #         delete_meeting_by_id(self.current_draft_id)
            #         self.current_draft_id = None
                
            #     QMessageBox.information(self, "Saved", "Record Saved successfully.")
            #     self.ui.saveBtn.setEnabled(False)
            #     QTimer.singleShot(1000, lambda: self.ui.saveBtn.setEnabled(True))
            #     self._load_saved_recordings()
            #     self._clear_generate_pages()
            #     self._set_page(self.ui.GeneratePage1)  # Navigate back to GeneratePage1
        else:
            QMessageBox.warning(self, "Error", "Failed to save the meeting.")

    def _save_log_to_database(self):
        if not self.current_meeting_id:
            QMessageBox.warning(self, "Error", "No meeting selected!")
            return

        # Create export dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Click Ok to Save Record")
        layout = QVBoxLayout()
        
        transcript_cb = QCheckBox("Export Transcript")
        minutes_cb = QCheckBox("Export Minutes")
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        layout.addWidget(transcript_cb)
        layout.addWidget(minutes_cb)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        if dialog.exec() != QDialog.Accepted:
            return

        # Get user choices
        export_transcript = transcript_cb.isChecked()
        export_minutes = minutes_cb.isChecked()
        
        # Handle export
        sections = []
        transcript = self.ui.logTranscriptDisplay.toPlainText().strip()
        minutes = self.ui.logMinutesDisplay.toPlainText().strip()
        t = self.ui.logTranscriptDisplay.toHtml().strip()
        
        if export_transcript and transcript:
            sections.append(("Meeting Transcript", transcript))
        if export_minutes and minutes:
            sections.append(("Meeting Minutes", minutes))
        
        if sections:
            path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "",
                "PDF Files (*.pdf);;Word Files (*.docx)"
            )
            if path:
                if path.endswith(".pdf"):
                    self._save_pdf(path, sections)
                elif path.endswith(".docx"):
                    self._save_word(path, sections)
                QMessageBox.information(self, "Exported", f"File saved to:\n{path}")

        # Check if this is a draft and modify title if needed
        title = self.current_log_title
        if title and title.startswith("Transcript Draft"):
            # Replace "Transcript Draft" with "Recording" but keep the date and time
            title = title.replace("Transcript Draft","Recording")
        # title = f"Recording {datetime.now().strftime('%m/%d/%Y at %I:%M %p')}" change the date and time

        # Update database
        success = save_meeting(
            self.file_name,
            title=title,  # Use the potentially modified title
            agenda=self.current_log_agenda,
            transcript=t,
            is_translated =self.is_translated,
            translated_transcript = self.translated_transcript,
            minutes=minutes,
            is_draft=0,  # Set is_draft to 0 when converting from draft to recording
            meeting_id=self.current_meeting_id
        )
        
        if success:
            QMessageBox.information(self, "Saved", "Meeting updated successfully!")
            self._load_saved_recordings()  # Refresh list
        else:
            QMessageBox.warning(self, "Error", "Failed to save changes!")

    def _clear_generate_pages(self):
        self.ui.agendaInput.clear()
        self.agendas.clear()
        self.ui.attendeesInput.clear()
        self.attendees.clear()
        self._update_transcript()
        self.ui.transcriptDisplay.clear()
        self.ui.minutesDisplay.clear()
        self.ui.uploadedFileLabel.setText("")
        self.speaker_map.clear()
        self.current_draft_id = None

    def _load_saved_recordings(self):
        self.ui.savedListWidget.clear()
        for meeting_id, title, is_draft in get_all_recordings():
            item = QListWidgetItem()
            self.ui.savedListWidget.addItem(item)

            item_widget = QWidget()
            layout = QHBoxLayout(item_widget)
            layout.setContentsMargins(5, 0, 5, 0)
            
            text_label = QLabel(title)
            text_label.setStyleSheet("""
                QLabel {
                    color: rgb(41, 28, 14);
                    font-family: 'Times New Roman';
                    font-size: 16px;
                    padding: 3px;
                    background-color: transparent;
                }
            """)
            text_label.setProperty("meeting_id", meeting_id)
            
            layout.addWidget(text_label)

            delete_btn = QPushButton("Delete")
            delete_btn.setFixedWidth(60)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color:  rgb(185, 128, 118);
                    color: white;
                    border-radius: 3px;
                    padding: 3px;
                }
                QPushButton:hover {
                    background-color: #e03131;
                }
            """)
            delete_btn.clicked.connect(lambda _, m_id=meeting_id: self._delete_meeting(m_id))

            layout.addStretch(1)
            layout.addWidget(delete_btn)
            self.ui.savedListWidget.setItemWidget(item, item_widget)

    def _delete_meeting(self, meeting_id):
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete this recording?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            if delete_meeting_by_id(meeting_id):
                QMessageBox.information(self, "Deleted", "Recording deleted successfully.")
                cur = self.ui.stackedWidget.currentWidget()
                if cur == self.ui.activityLogPage and meeting_id == self.current_meeting_id:
                    self._set_page(self.ui.activityListPage)
                self._load_saved_recordings()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete the recording.")


    def _extract_minutes_sections(self, text):
        """Extract sections from text based on key headers"""
        sections = {}
        
        # Match the exact headers in the document
        keys = [
            "Meeting Date",
            "ATTENDEES",
            "MEETING AGENDA",
            "MEETING OVERVIEW",
            "DISCUSSION POINTS",
            "ACTION ITEMS"
        ]


        for i, key in enumerate(keys):
                start_pos = text.find(key + ":")
                if start_pos != -1:
                    start_pos += len(key) + 1
                    end_pos = len(text)
                    for next_key in keys:
                        next_pos = text.find(next_key + ":", start_pos)
                        if next_pos != -1 and next_pos < end_pos:
                            end_pos = next_pos
                    sections[key] = text[start_pos:end_pos].strip()
            
        return sections

    def parse_log_minutes(self, minutes):
        sections = self._extract_minutes_sections(minutes)

        # Build the minutes HTML
        html_content = f"""
        <b>MINUTES OF THE MEETING</b>
        <br>
        <b>Meeting Date: {sections.get("Meeting Date", "N/A")}</b>
        <br><br>

        <br><b>ATTENDEES:</b><br>
        {self.pre_wrap(sections.get("ATTENDEES", "No attendees recorded"))}<br>

        <br><b>MEETING AGENDA:</b>
        {self.pre_wrap(sections.get("MEETING AGENDA", "No agenda items recorded"))}

        <br><b>MEETING OVERVIEW:</b><br>
        {self.pre_wrap(sections.get("MEETING OVERVIEW", "No overview provided"))}<br>

        <b>DISCUSSION POINTS:</b><br> 
        {self.pre_wrap(sections.get("DISCUSSION POINTS", "No discussion points recorded"))}<br> 

        <b>ACTION ITEMS:</b>
        {self.pre_wrap(sections.get("ACTION ITEMS", "No action items recorded"))}
        """
        return html_content

    def _load_selected_log(self, item):
        widget = self.ui.savedListWidget.itemWidget(item)
        if widget:
            label = widget.findChild(QLabel)
            if label:
                meeting_id = label.property("meeting_id")
                if meeting_id:
                    self.current_meeting_id = meeting_id
                    file_name, title, agenda, transcript, is_translated, translated_transcript, minutes = get_meeting_by_id(meeting_id)
                    formatted_minutes = self.parse_log_minutes(minutes)
                    self.file_name = file_name
                    self.current_log_title = title
                    self.agenda_text = agenda
                    self.ui.logTranscriptDisplay.setHtml(transcript)
                    self.ui.logMinutesDisplay.setHtml(formatted_minutes)
                    self.transcript = transcript
                    self.minutes = minutes
                    self.is_translated = is_translated
                    self.translated_transcript = translated_transcript
                    self._set_page(self.ui.activityLogPage)

    def _set_page(self, page):
        self.ui.stackedWidget.setCurrentWidget(page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())