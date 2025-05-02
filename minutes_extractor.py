import json
import os
import ollama
import time
import tiktoken
import concurrent.futures
from functools import partial

class ModelConfig:
    """
    Central configuration class for LLM model settings
    """
    def __init__(self, model_name="llama-3.1-8b-q4:latest", temperature=0.5, mirostat=2.0):
        self.model_name = model_name
        self.temperature = temperature
        self.mirostat = mirostat
    
    def get_chat_options(self, custom_temperature=None, custom_mirostat=None):
        """Get the options dictionary for ollama.chat"""
        temp = custom_temperature if custom_temperature is not None else self.temperature
        mirostat = custom_mirostat if custom_mirostat is not None else self.mirostat
        return {"temperature": temp, "mirostat": mirostat}

class TranscriptChunker:
    def __init__(self, max_chunk_size=4096, overlap_size=500):
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
    def chunk_transcript(self, transcript):
        """
        Split a long transcript into manageable chunks with overlapping context
        using tiktoken for accurate token counting
        
        Args:
            transcript (str): The full transcript text
                
        Returns:
            list: List of transcript chunks
        """
        # If transcript is shorter than max_chunk_size, return it as a single chunk
        tokens = self.encoder.encode(transcript)
        print(len(tokens))
        if len(tokens) <= self.max_chunk_size:
            return [transcript]
        
        # Split transcript by lines
        lines = transcript.split('\n')
        
        chunks = []
        current_chunk_lines = []
        current_chunk_tokens = []
        overlap_buffer_lines = []
        overlap_buffer_tokens = []
        
        for line in lines:
            line_tokens = self.encoder.encode(line + '\n')  # Include newline in token count
            
            # If adding this line would exceed the max chunk size and we already have content
            if current_chunk_tokens and len(current_chunk_tokens) + len(line_tokens) > self.max_chunk_size:
                # Save the current chunk
                chunks.append('\n'.join(current_chunk_lines))
                
                # Set up the next chunk with overlap
                # Find speaker markers in the overlap buffer to ensure we start with a speaker
                overlap_text = '\n'.join(overlap_buffer_lines)
                
                # Initialize the next chunk with the overlap buffer
                current_chunk_lines = overlap_buffer_lines.copy()
                current_chunk_tokens = overlap_buffer_tokens.copy()
                
                # Reset overlap buffer for the next chunk
                overlap_buffer_lines = []
                overlap_buffer_tokens = []
            
            # Add the current line to the chunk
            current_chunk_lines.append(line)
            current_chunk_tokens.extend(line_tokens)
            
            # Maintain the overlap buffer with the most recent lines
            overlap_buffer_lines.append(line)
            overlap_buffer_tokens.extend(line_tokens)
            
            # Keep the overlap buffer at the appropriate size
            while len(overlap_buffer_tokens) > self.overlap_size:
                removed_line = overlap_buffer_lines.pop(0)
                removed_tokens = self.encoder.encode(removed_line + '\n')
                overlap_buffer_tokens = overlap_buffer_tokens[len(removed_tokens):]
        
        # Add the last chunk if it's not empty
        if current_chunk_lines:
            chunks.append('\n'.join(current_chunk_lines))
        
        # Ensure each chunk starts with a speaker marker if possible
        for i in range(1, len(chunks)):
            if not chunks[i].strip().startswith("SPEAKER"):
                # Find the first speaker marker
                speaker_index = chunks[i].find("SPEAKER")
                if speaker_index > 0:
                    # Move the text before the speaker marker to the previous chunk
                    chunks[i-1] += chunks[i][:speaker_index]
                    chunks[i] = chunks[i][speaker_index:]
        
        return chunks

class PromptGenerator:
    def __init__(self):
        pass
    
    def generate_dynamic_agenda_prompt(self, transcript, output_language="English"):
        """Generate a prompt to identify agenda items dynamically"""
        return f"""
        Based on the following meeting transcript, identify the TOP meaningful agendas/meeting topics dynamically.
        Make sure to focus on the most important topics, without redundant or similar context.
        
        Transcript:
        {transcript}
        
        Respond with a JSON object in the following format:
        {{
            "agenda_items": ["topic1", "topic2", "topic3"]
        }}
        
        Include only the most significant topics discussed in the meeting.
        Your response must be in {output_language} regardless of the language in the transcript.
        """

    def generate_overview_prompt(self, transcript, agenda_items, output_language="English"):
        """Generate a prompt to create a meeting overview"""
        return f"""
        Based on the following meeting transcript and agenda items, write a 1 paragraph short and concise meeting overview.
        The overview should capture the essence of the meeting without delving too much into details.
        
        Transcript:
        {transcript}
        
        Agenda Items:
        {json.dumps(agenda_items)}
        
        Respond with a JSON object in the following format:
        {{
            "meeting_overview": "Your concise meeting overview here."
        }}
        
        Your response must be in {output_language} regardless of the language in the transcript.
        """

    def generate_discussion_prompt(self, transcript, agenda_items, output_language="English"):
        """Generate a prompt to extract key points for each agenda item"""
        return f"""
        Based on the following meeting transcript and agenda items, extract and summarize the top most important key points
        for each agenda item. Each key point should be:
        1. A concise summary (not a verbatim quote)
        2. Written in third person point of view
        3. Include the speaker's ID
        4. Capture the essence of what was said without being too detailed
        
        Do NOT include direct quotes. Instead, paraphrase and summarize the key ideas.
        
        Transcript:
        {transcript}
        
        Agenda Items:
        {json.dumps(agenda_items)}
        
        Respond with a JSON object in the following format:
        {{
            "discussion_points": [
                {{
                    "agenda_item": "topic1",
                    "points": [
                        {{
                            "speaker": "SPEAKER X", 
                            "point": "Concise summary of the key point in third person"
                        }},
                        {{
                            "speaker": "SPEAKER Y", 
                            "point": "Concise summary of the key point in third person"
                        }}
                    ]
                }},
                {{
                    "agenda_item": "topic2",
                    "points": [
                        {{
                            "speaker": "SPEAKER Z", 
                            "point": "Concise summary of the key point in third person"
                        }}
                    ]
                }}
            ]
        }}
        
        Important guidelines:
        - Each point should be 1-2 sentences maximum
        - Focus on the main idea, not every detail
        - Combine related ideas from the same speaker
        - Remove filler words and repetitions
        - Maintain the original meaning but express it more concisely
        
        Your response must be in {output_language} regardless of the language in the transcript.
        """

    def generate_action_prompt(self, transcript, output_language="English"):
        """Generate a prompt to extract action items"""
        return f"""
        Based on the following meeting transcript, extract all proposed action items.
        A proposed action item is a future task that someone has committed to doing.
        
        Transcript:
        {transcript}
        
        Respond with a JSON object in the following format:
        {{
            "action_items": [
                {{"assignee": "Speaker X", "action": "Description of the proposed action to be taken"}},
                {{"assignee": "Speaker Y", "action": "Description of the proposed action to be taken"}}
            ]
        }}
        
        Include only clear proposed action items where someone has committed to doing something specific.
        Your response must be in {output_language} regardless of the language in the transcript.
        """

class AgendaProcessor:
    def __init__(self, prompt_generator, model_config, output_language="English"):
        self.prompt_generator = prompt_generator
        self.model_config = model_config
        self.output_language = output_language
    
    def process_chunk_for_agenda(self, chunk, chunk_index, total_chunks):
        """Process a single chunk for agenda items"""
        print(f"Processing chunk {chunk_index+1}/{total_chunks} for agenda items")
        agenda_prompt = self.prompt_generator.generate_dynamic_agenda_prompt(chunk, self.output_language)
        
        agenda_response = ollama.chat(
            model=self.model_config.model_name, 
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that extracts meeting agenda items from transcripts. Always respond in {self.output_language} regardless of the input language."},
                {"role": "user", "content": agenda_prompt}
            ], 
            format="json",
            options=self.model_config.get_chat_options()
        )
        
        try:
            agenda_result = json.loads(agenda_response['message']['content'])
            return agenda_result.get('agenda_items', [])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing chunk {chunk_index+1} for agenda items: {e}")
            print(f"Raw response: {agenda_response['message']['content']}")
            return []
    
    def identify_agenda_items_from_chunks_parallel(self, transcript_chunks, max_workers=None):
        """
        Identify agenda items from transcript chunks in parallel
        
        Args:
            transcript_chunks (list): List of transcript text chunks
            max_workers (int, optional): Maximum number of worker processes
            
        Returns:
            list: Identified agenda items
        """
        all_agenda_items = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a list of futures
            future_to_chunk = {
                executor.submit(
                    self.process_chunk_for_agenda, 
                    chunk, 
                    i, 
                    len(transcript_chunks)
                ): i for i, chunk in enumerate(transcript_chunks)
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_chunk):
                try:
                    chunk_agenda_items = future.result()
                    all_agenda_items.extend(chunk_agenda_items)
                except Exception as e:
                    chunk_index = future_to_chunk[future]
                    print(f"Exception processing chunk {chunk_index+1} for agenda: {e}")
        
        # Consolidate and deduplicate agenda items
        consolidated_items = self.consolidate_agenda_items(all_agenda_items)
        return consolidated_items
    
    def consolidate_agenda_items(self, agenda_items):
        """
        Consolidate and deduplicate agenda items
        
        Args:
            agenda_items (list): List of all extracted agenda items
            
        Returns:
            list: Consolidated list of unique agenda items
        """
        if not agenda_items:
            return []
        
        # Create a consolidated prompt to refine the agenda items
        consolidated_prompt = f"""
        I have extracted the following potential agenda items from different parts of a meeting transcript:
        {json.dumps(agenda_items)}
        
        Please consolidate these into a concise list of 3-7 main agenda items, removing duplicates and combining similar topics.
        
        Respond with a JSON object in the following format:
        {{
            "agenda_items": ["topic1", "topic2", "topic3"]
        }}
        """
        
        consolidation_response = ollama.chat(
            model=self.model_config.model_name, 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that consolidates meeting agenda items."},
                {"role": "user", "content": consolidated_prompt}
            ], 
            format="json",
            options=self.model_config.get_chat_options(0)  # Use temperature 0 for deterministic results
        )
        
        try:
            consolidation_result = json.loads(consolidation_response['message']['content'])
            return consolidation_result.get('agenda_items', [])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error consolidating agenda items: {e}")
            print(f"Raw response: {consolidation_response['message']['content']}")
            # Fall back to basic deduplication
            return list(set(agenda_items))

class OverviewProcessor:
    def __init__(self, prompt_generator, model_config, output_language="English"):
        self.prompt_generator = prompt_generator
        self.model_config = model_config
        self.output_language = output_language
    
    def process_chunk_for_overview(self, chunk, agenda_items, chunk_index, total_chunks):
        """Process a single chunk for meeting overview"""
        print(f"Processing chunk {chunk_index+1}/{total_chunks} for overview")
        overview_prompt = self.prompt_generator.generate_overview_prompt(chunk, agenda_items, self.output_language)
        
        overview_response = ollama.chat(
            model=self.model_config.model_name, 
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that creates concise meeting overviews. Always respond in {self.output_language} regardless of the input language."},
                {"role": "user", "content": overview_prompt}
            ], 
            format="json",
            options=self.model_config.get_chat_options()
        )
        
        try:
            overview_result = json.loads(overview_response['message']['content'])
            return overview_result.get('meeting_overview', '')
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing chunk {chunk_index+1} for overview: {e}")
            print(f"Raw response: {overview_response['message']['content']}")
            return ""
    
    def generate_overview_from_chunks_parallel(self, transcript_chunks, agenda_items, max_workers=None):
        """
        Generate meeting overview from transcript chunks in parallel
        
        Args:
            transcript_chunks (list): List of transcript text chunks
            agenda_items (list): List of identified agenda items
            max_workers (int, optional): Maximum number of worker processes
            
        Returns:
            str: Meeting overview
        """
        chunk_summaries = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a list of futures
            future_to_chunk = {
                executor.submit(
                    self.process_chunk_for_overview, 
                    chunk, 
                    agenda_items, 
                    i, 
                    len(transcript_chunks)
                ): i for i, chunk in enumerate(transcript_chunks)
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_chunk):
                try:
                    chunk_summary = future.result()
                    if chunk_summary:
                        chunk_summaries.append(chunk_summary)
                except Exception as e:
                    chunk_index = future_to_chunk[future]
                    print(f"Exception processing chunk {chunk_index+1} for overview: {e}")
        
        # Combine chunk summaries into a final overview
        if chunk_summaries:
            if len(chunk_summaries) == 1:
                return chunk_summaries[0]
            else:
                return self.consolidate_overviews(chunk_summaries, agenda_items)
        else:
            return "No overview could be generated from the transcript."
    
    def consolidate_overviews(self, chunk_summaries, agenda_items):
        """
        Consolidate multiple chunk overviews into a single cohesive overview
        
        Args:
            chunk_summaries (list): List of overview summaries from each chunk
            agenda_items (list): List of identified agenda items
            
        Returns:
            str: Consolidated meeting overview
        """
        # Create a consolidated prompt
        consolidated_prompt = f"""
        I have generated the following overview summaries from different parts of a meeting transcript:
        {json.dumps(chunk_summaries)}
        
        The meeting discussed these agenda items:
        {json.dumps(agenda_items)}
        
        Please consolidate these summaries into a single coherent overview paragraph that captures the essence of the meeting.
        
        Respond with a JSON object in the following format:
        {{
            "meeting_overview": "Your consolidated meeting overview here."
        }}
        """
        
        consolidation_response = ollama.chat(
            model=self.model_config.model_name, 
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that consolidates meeting overviews. Always respond in {self.output_language} regardless of the input language."},
                {"role": "user", "content": consolidated_prompt}
            ], 
            format="json",
            options=self.model_config.get_chat_options(0)  # Use temperature 0 for deterministic results
        )
        
        try:
            consolidation_result = json.loads(consolidation_response['message']['content'])
            return consolidation_result.get('meeting_overview', '')
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error consolidating overviews: {e}")
            print(f"Raw response: {consolidation_response['message']['content']}")
            # Fall back to concatenation
            return " ".join(chunk_summaries)

class DiscussionProcessor:
    def __init__(self, prompt_generator, model_config, output_language="English"):
        self.prompt_generator = prompt_generator
        self.model_config = model_config
        self.output_language = output_language
    
    def process_chunk_for_discussion(self, chunk, agenda_items, chunk_index, total_chunks):
        """Process a single chunk for discussion points"""
        print(f"Processing chunk {chunk_index+1}/{total_chunks} for discussion points")
        discussion_prompt = self.prompt_generator.generate_discussion_prompt(chunk, agenda_items, self.output_language)
        
        discussion_response = ollama.chat(
            model=self.model_config.model_name, 
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that extracts the top key points from meeting transcripts. Always respond in {self.output_language} regardless of the input language."},
                {"role": "user", "content": discussion_prompt}
            ], 
            format="json",
            options=self.model_config.get_chat_options()
        )
        
        try:
            discussion_result = json.loads(discussion_response['message']['content'])
            return discussion_result.get('discussion_points', [])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing chunk {chunk_index+1} for discussion points: {e}")
            print(f"Raw response: {discussion_response['message']['content']}")
            return []
    
    def extract_discussion_points_from_chunks_parallel(self, transcript_chunks, agenda_items, max_workers=None):
        """
        Extract discussion points from transcript chunks in parallel
        
        Args:
            transcript_chunks (list): List of transcript text chunks
            agenda_items (list): List of identified agenda items
            max_workers (int, optional): Maximum number of worker processes
            
        Returns:
            list: Discussion points organized by agenda item
        """
        all_discussion_points = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a list of futures
            future_to_chunk = {
                executor.submit(
                    self.process_chunk_for_discussion, 
                    chunk, 
                    agenda_items, 
                    i, 
                    len(transcript_chunks)
                ): i for i, chunk in enumerate(transcript_chunks)
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_chunk):
                try:
                    chunk_points = future.result()
                    all_discussion_points.extend(chunk_points)
                except Exception as e:
                    chunk_index = future_to_chunk[future]
                    print(f"Exception processing chunk {chunk_index+1} for discussion points: {e}")
        
        # Consolidate discussion points by agenda item
        return self.consolidate_discussion_points(all_discussion_points, agenda_items)
    
    def consolidate_discussion_points(self, all_points, agenda_items):
        """
        Consolidate discussion points by agenda item
        
        Args:
            all_points (list): List of all extracted discussion points from all chunks
            agenda_items (list): List of identified agenda items
            
        Returns:
            list: Consolidated discussion points organized by agenda item
        """
        # Create a dictionary to store points for each agenda item
        agenda_point_map = {item: [] for item in agenda_items}
        
        # Collect all points for each agenda item
        for point_group in all_points:
            agenda_item = point_group.get('agenda_item', '')
            points = point_group.get('points', [])
            
            # Find the best matching agenda item
            best_match = self.find_best_matching_agenda_item(agenda_item, agenda_items)
            if best_match:
                agenda_point_map[best_match].extend(points)
        
        # Format the consolidated points
        consolidated_points = []
        for agenda_item, points in agenda_point_map.items():
            # Remove duplicates
            unique_points = []
            seen_points = set()
            
            for point in points:
                point_text = point.get('point', '').lower()
                if point_text and point_text not in seen_points:
                    seen_points.add(point_text)
                    unique_points.append(point)
            
            if unique_points:
                consolidated_points.append({
                    "agenda_item": agenda_item,
                    "points": unique_points
                })
        
        return consolidated_points
    
    def find_best_matching_agenda_item(self, source_item, agenda_items):
        """
        Find the best matching agenda item from the list
        
        Args:
            source_item (str): The source agenda item to match
            agenda_items (list): List of target agenda items
            
        Returns:
            str: The best matching agenda item
        """
        if source_item in agenda_items:
            return source_item
        
        # Simple matching - find the agenda item with most word overlap
        source_words = set(source_item.lower().split())
        best_match = None
        best_overlap = 0
        
        for item in agenda_items:
            item_words = set(item.lower().split())
            overlap = len(source_words.intersection(item_words))
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = item
        
        # If no good match found, use the first agenda item
        if not best_match and agenda_items:
            best_match = agenda_items[0]
        
        return best_match

class ActionProcessor:
    def __init__(self, prompt_generator, model_config, output_language="English"):
        self.prompt_generator = prompt_generator
        self.model_config = model_config
        self.output_language = output_language
    
    def process_chunk_for_action(self, chunk, chunk_index, total_chunks):
        """Process a single chunk for action items"""
        print(f"Processing chunk {chunk_index+1}/{total_chunks} for action items")
        action_prompt = self.prompt_generator.generate_action_prompt(chunk, self.output_language)
        
        action_response = ollama.chat(
            model=self.model_config.model_name, 
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that extracts future TO-DO action items from meeting transcripts. Always respond in {self.output_language} regardless of the input language."},
                {"role": "user", "content": action_prompt}
            ], 
            format="json",
            options=self.model_config.get_chat_options(custom_temperature=0.2, custom_mirostat= 2.0)  # Use a higher temperature for more creative responses
        )
        
        try:
            action_result = json.loads(action_response['message']['content'])
            return action_result.get('action_items', [])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing chunk {chunk_index+1} for action items: {e}")
            print(f"Raw response: {action_response['message']['content']}")
            return []
    
    def extract_action_items_from_chunks_parallel(self, transcript_chunks, max_workers=None):
        """
        Extract action items from transcript chunks in parallel
        
        Args:
            transcript_chunks (list): List of transcript text chunks
            max_workers (int, optional): Maximum number of worker processes
            
        Returns:
            list: Extracted action items
        """
        all_action_items = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a list of futures
            future_to_chunk = {
                executor.submit(
                    self.process_chunk_for_action, 
                    chunk, 
                    i, 
                    len(transcript_chunks)
                ): i for i, chunk in enumerate(transcript_chunks)
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_chunk):
                try:
                    chunk_actions = future.result()
                    all_action_items.extend(chunk_actions)
                except Exception as e:
                    chunk_index = future_to_chunk[future]
                    print(f"Exception processing chunk {chunk_index+1} for action items: {e}")
        
        # Deduplicate action items
        return self.deduplicate_action_items(all_action_items)
    
    def deduplicate_action_items(self, action_items):
        """
        Deduplicate action items
        
        Args:
            action_items (list): List of all extracted action items
            
        Returns:
            list: Deduplicated action items
        """
        unique_actions = []
        seen_actions = set()
        
        for item in action_items:
            # Create a signature for the action item
            assignee = item.get('assignee', '').lower()
            action = item.get('action', '').lower()
            signature = f"{assignee}:{action}"
            
            if signature not in seen_actions:
                seen_actions.add(signature)
                unique_actions.append(item)
        
        return unique_actions

class MeetingMinutesExtractor:
    def __init__(self, model_config=None, output_language="English", max_workers=None):
        self.output_language = output_language
        self.max_workers = max_workers
        
        # Initialize model configuration
        self.model_config = model_config if model_config else ModelConfig()
        
        # Initialize components
        self.transcript_chunker = TranscriptChunker()
        self.prompt_generator = PromptGenerator()
        self.agenda_processor = AgendaProcessor(self.prompt_generator, self.model_config, output_language)
        self.overview_processor = OverviewProcessor(self.prompt_generator, self.model_config, output_language)
        self.discussion_processor = DiscussionProcessor(self.prompt_generator, self.model_config, output_language)
        self.action_processor = ActionProcessor(self.prompt_generator, self.model_config, output_language)
    
    def extract_meeting_minutes(self, transcript, agenda=None):
        """
        Extract meeting minutes from a transcript file using the configured LLM model
        with parallel processing of transcript chunks
        
        Args:
            transcript (str): The transcript text to process
            agenda (str, optional): List of agenda items
        
        Returns:
            dict: Structured meeting minutes
        """
 
        
        # Process transcript if it's long
        transcript_chunks = self.transcript_chunker.chunk_transcript(transcript)
        print(f"Transcript split into {len(transcript_chunks)} chunks for processing")
        
        # Check if agenda file exists and is not empty
        agenda_items = []
        if agenda:
            agenda_items = [line.strip() for line in agenda if line.strip()]
            # print(agenda_items)
        else:
            # Dynamically identify agenda items in parallel
            agenda_items = self.agenda_processor.identify_agenda_items_from_chunks_parallel(
                transcript_chunks, self.max_workers
            )
        
        # Generate meeting overview in parallel
        overview = self.overview_processor.generate_overview_from_chunks_parallel(
            transcript_chunks, agenda_items, self.max_workers
        )
        
        # Extract discussion points for each agenda item in parallel
        discussion_points = self.discussion_processor.extract_discussion_points_from_chunks_parallel(
            transcript_chunks, agenda_items, self.max_workers
        )
        
        # Extract action items in parallel
        action_items = self.action_processor.extract_action_items_from_chunks_parallel(
            transcript_chunks, self.max_workers
        )
        
        # Combine all results into a single structure
        meeting_minutes = {
            "meeting_overview": overview,
            "agenda_items": agenda_items,
            "discussion_points": discussion_points,
            "action_items": action_items
        }
        
        return meeting_minutes
    
    def save_minutes_to_file(self, minutes, output_path):
        """Save meeting minutes to a file"""
        with open(output_path, 'w') as f:
            json.dump(minutes, f, indent=2)

#     def format_meeting_minutes(self, minutes):
#         formatted_text = f"Meeting Overview:\n{minutes['meeting_overview']}\n\n"
        
#         formatted_text += "Agenda Items:\n"
#         for i, item in enumerate(minutes['agenda_items'], 1):
#             formatted_text += f"{i}. {item}\n"
#         formatted_text += "\n"
        
#         formatted_text += "Discussion Points:\n"
#         for agenda in minutes['discussion_points']:
#             formatted_text += f"\n{agenda['agenda_item']}\n"
#             for point in agenda['points']:
#                 formatted_text += f"- {point['speaker']}: {point['point']}\n"
        
#         formatted_text += "\nAction Items:\n"
#         for action in minutes['action_items']:
#             formatted_text += f"- {action['assignee']}: {action['action']}\n"
        
#         return formatted_text


def main():
    # Example usage with custom model configuration
    transcript_path = "testfiles/weekly_sample.txt"
    agenda_path = "testfiles/test_agenda.txt"
    output_path = "testfiles/Risa.json"
    output_language = "English"
    
    # Configure the model - easy to change for all components at once
    model_config = ModelConfig(
        model_name="yissus/llama-3.1-8b-q4:latest",  # Change this to use a different model
        temperature=0.5,
        mirostat=2.0
    )
    
    # Create extractor with the model configuration
    extractor = MeetingMinutesExtractor(
        model_config=model_config,
        output_language=output_language,
        max_workers=None  # Let Python decide the optimal number based on system
    )

    with open(transcript_path, 'r') as f:
        transcript = f.read()
    with open(agenda_path, 'r') as f:
        agenda = f.readlines()
    
    start_time = time.time()
    minutes = extractor.extract_meeting_minutes(transcript=transcript, agenda=agenda)
    extractor.save_minutes_to_file(minutes, output_path)
    
    
    print(f"Meeting minutes saved to {output_path}")
    elapsed_time = time.time() - start_time
    print(f"Total Time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()