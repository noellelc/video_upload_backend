import json
import boto3
from boto3 import Session
from contextlib import closing
from tempfile import gettempdir
import os
import urllib.request

BUCKET_NAME = "devdiv-hackweek-translated"

s3 = boto3.resource('s3')
transcribe = boto3.client('transcribe')
translate = boto3.client('translate')

def lambda_handler(event, context):
    job_name = event['detail']['TranscriptionJobName']
    job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(uri)
    
    content = urllib.request.urlopen(uri).read().decode('UTF-8')

    data = json.loads(content)
    
    print('parsing transcription into sentences')
    phrases = []
    phrase = {}
    for item in data['results']['items']:
        if (len(phrase) == 0) & (item['type'] == 'pronunciation'):
            phrase['word'] = item['alternatives'][0]['content']
            phrase['start_time'] = float(item['start_time'])
            phrase['end_time'] = float(item['end_time'])
        elif (item['type'] == 'pronunciation'):
            phrase['word'] = phrase['word'] + ' ' + item['alternatives'][0]['content']
            phrase['end_time'] = float(item['end_time'])
        elif (len(phrase) != 0) & (item['alternatives'][0]['content'] == '.'):
            #End of sentence
            phrases.append(phrase)
            phrase = {}
        elif (len(phrase) != 0):
            phrase['word'] = phrase['word'] + ' ' + item['alternatives'][0]['content']
    
    print(f'total sentences found: {len(phrases)}')
    
    i = 1
    tempDir = gettempdir()
    outputTxt = os.path.join(tempDir, "translated_content.txt")
    output = os.path.join(tempDir, "translated_content_at_speed.mp3")
    
    for phrase in phrases:
        phrase['duration'] = (phrase['end_time'] - phrase['start_time'])*1000
        result = translate.translate_text(Text=phrase['word'], SourceLanguageCode="en", TargetLanguageCode="hi")
        phrase['translation'] = result.get('TranslatedText')
        transcribe_translation(phrase['translation'], outputTxt)
        phrase['actual_time'] = speech_generation(phrase['translation'],phrase['duration'], output)
        i = i + 1
    
    new_filename = job_name[:job_name.rindex('.')]
    
    s3.Bucket(BUCKET_NAME).upload_file(
        outputTxt,
        new_filename + '.txt')
        
    s3.Bucket(BUCKET_NAME).upload_file(
        output,
        new_filename + '.mp3')
    
def transcribe_translation(text, txtFile):
    with open(txtFile, "a") as file:
        file.write(text + ' | ')

def speech_generation(content, duration_ms, output):
        session = Session()
        polly = session.client("polly")
    
        speed = '100'
        intext = content
        desired_time_in_ms = duration_ms
    
        text = f'<speak><prosody rate="{speed}%">{intext}<mark name="ttb"/></prosody></speak>'
        response = polly.synthesize_speech(
                Text= text, 
                OutputFormat = "json",
                Engine = 'standard',
                VoiceId = "Aditi",
                LanguageCode = 'hi-IN',
                TextType = 'ssml',
                SpeechMarkTypes = ("sentence", "ssml")
            )
        
        #find the time it takes to render it at speed 100
        stream = response["AudioStream"].read().decode()
        t1 = stream.replace('\n',',')
        t2 = '[' + t1[:-1] + ']'
        t2 = json.loads(t2)
        actual_time = t2[-1]['time']
        
        """ 
        ##calculate how much we will need to speed it by -- we can use int or round
        speed = str(int(100*actual_time/desired_time_in_ms))
    
        #now plug in the new speed
        text = '<speak>'+'<prosody rate="'+speed+'%">'+intext+ '<mark name="ttb"/>' + '</prosody>'+'</speak>'
        """
        response = polly.synthesize_speech(
            Text = text, 
            OutputFormat = "mp3",
            Engine = 'standard',
            VoiceId = "Aditi",
            LanguageCode = 'hi-IN',
            TextType = 'ssml',
        )
        
        if "AudioStream" in response:
            # Note: Closing the stream is important because the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "ab") as file:
                        file.write(stream.read())
                    return actual_time
                    
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
    
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)