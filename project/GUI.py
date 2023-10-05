import tkinter as tk
import tkinter.font as font
import cv2
import numpy as np
import six.moves.urllib as urllib
import sys
from googletrans import Translator
import time
import tensorflow as tf
from datetime import datetime
import pyttsx3 as tts
from threading import Thread
from collections import defaultdict
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from urllib.request import urlopen
from tkinter import ttk
window = tk.Tk()
engine = tts.init()
window.title("Transign")
PATH_TO_LABELS = 'training/labelmap.pbtxt'
PATH_TO_MODEL = './saved_model'
PATH_TO_LOGO = './logo.png'
PHRASE = ["i am fine","how are you","what is your"]
SWITCH = ["i fine","how you","what your"]
TRANSLATE = tk.IntVar()
FONT = font.Font(family="Helvetica",size="16",weight="bold")
WINNAME = 'Press "Q" to Exit'
CHOSEN_LANGUAGE = tk.StringVar()
LANGUAGES = {
    'Afrikaans' : 'af',
    'Albanian' : 'sq',
    'Amharic' : 'am',
    'Arabic' : 'ar',
    'Armenian' : 'hy',
    'Azerbaijani' : 'az',
    'Basque' : 'eu',
    'Belarusian' : 'be',
    'Bengali' : 'bn',
    'Bosnian' : 'bs',
    'Bulgarian' : 'bg',
    'Catalan' : 'ca',
    'Cebuano' : 'ceb',
    'Chichewa' : 'ny',
    'Chinese (Simplified)' : 'zh-cn',
    'Chinese (Traditional)' : 'zh-tw',
    'Corsican' : 'co',
    'Croatian' : 'hr',
    'Czech' : 'cs',
    'Danish' : 'da',
    'Dutch' : 'nl',
    'English' : 'en',
    'Esperanto' : 'eo',
    'Estonian' : 'et',
    'Filipino' : 'tl',
    'Finnish' : 'fi',
    'French' : 'fr',
    'Frisian' : 'fy',
    'Galician' : 'gl',
    'Georgian' : 'ka',
    'German' : 'de',
    'Greek' : 'el',
    'Gujarati' : 'gu',
    'Haitian Creole' : 'ht',
    'Hausa' : 'ha',
    'Hawaiian' : 'haw',
    'Hebrew' : 'iw',
    'Hebrew' : 'he',
    'Hindi' : 'hi',
    'Hmong' : 'hmn',
    'Hungarian' : 'hu',
    'Icelandic' : 'is',
    'Igbo' : 'ig',
    'Indonesian' : 'id',
    'Irish' : 'ga',
    'Italian' : 'it',
    'Japanese' : 'ja',
    'Javanese' : 'jw',
    'Kannada' : 'kn',
    'Kazakh' : 'kk',
    'Khmer' : 'km',
    'Korean' : 'ko',
    'Kurdish (Kurmanji)' : 'ku',
    'Kyrgyz' : 'ky',
    'Lao' : 'lo',
    'Latin' : 'la',
    'Latvian' : 'lv',
    'Lithuanian' : 'lt',
    'Luxembourgish' : 'lb',
    'Macedonian' : 'mk',
    'Malagasy' : 'mg',
    'Malay' : 'ms',
    'Malayalam' : 'ml',
    'Maltese' : 'mt',
    'Maori' : 'mi',
    'Marathi' : 'mr',
    'Mongolian' : 'mn',
    'Myanmar (Burmese)' : 'my',
    'Nepali' : 'ne',
    'Norwegian' : 'no',
    'Odia' : 'or',
    'Pashto' : 'ps',
    'Persian' : 'fa',
    'Polish' : 'pl',
    'Portuguese' : 'pt',
    'Punjabi' : 'pa',
    'Romanian' : 'ro',
    'Russian' : 'ru',
    'Samoan' : 'sm',
    'Scots Gaelic' : 'gd',
    'Serbian' : 'sr',
    'Sesotho' : 'st',
    'Shona' : 'sn',
    'Sindhi' : 'sd',
    'Sinhala' : 'si',
    'Slovak' : 'sk',
    'Slovenian' : 'sl',
    'Somali' : 'so',
    'Spanish' : 'es',
    'Sundanese' : 'su',
    'Swahili' : 'sw',
    'Swedish' : 'sv',
    'Tajik' : 'tg',
    'Tamil' : 'ta',
    'Telugu' : 'te',
    'Thai' : 'th',
    'Turkish' : 'tr',
    'Ukrainian' : 'uk',
    'Urdu' : 'ur',
    'Uyghur' : 'ug',
    'Uzbek' : 'uz',
    'Vietnamese' : 'vi',
    'Welsh' : 'cy',
    'Xhosa' : 'xh',
    'Yiddish' : 'yi',
    'Yoruba' : 'yo',
    'Zulu' : 'zu', }
utils_ops.tf = tf.compat.v1
tf.gfile = tf.io.gfile

WIDTH = 500
HEIGHT = 800

def prevent_exit():
    pass

def translate_speech(data):
    tler = Translator()
    end_lang = "en"
    if not CHOSEN_LANGUAGE.get() == "" :
        end_lang = LANGUAGES[CHOSEN_LANGUAGE.get()]
    tl = tler.translate(data,src="en",dest=end_lang)
    return tl.text

def msg_box(cb,btn,optn):
    btn.config(state=tk.DISABLED)
    temp_window = tk.Tk()
    temp_window.title("WiFi check")
    temp_label = tk.Label(temp_window,text="Hold on, checking for internet connectivity")
    temp_label.pack(side=tk.TOP,fill="both",expand=True)
    thread_int = Thread(target=check_internet,args=(cb,temp_label,temp_window,btn,optn))
    thread_int.start()
    temp_window.mainloop()

def check_internet(c,l,w,b,o):
    try:
        response = urlopen('https://www.google.com/', timeout=3)
        c.config(state=tk.NORMAL)
        l.config(text="Connected")
        time.sleep(1)
        b.config(state=tk.NORMAL)
        w.destroy()
    except:
        c.config(state=tk.DISABLED)
        if TRANSLATE.get() == 1 :
            c.deselect()
        o.config(state=tk.DISABLED)
        l.config(text="Not connected")
        time.sleep(1)
        b.config(state=tk.NORMAL)
        w.destroy()
    
def convert_speech(data,tb_trans):
    for i in range(len(PHRASE)):
        if SWITCH[i] in data:
            data = data.replace(SWITCH[i],PHRASE[i])
    if TRANSLATE.get() == 1 and not data is None:
        data = translate_speech(data)
    tb_trans["text"] = data
    engine.say(data)
    engine.runAndWait()


def load_data():
    model = tf.saved_model.load(PATH_TO_MODEL)
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
    return model,category_index

def run_inference(model, image):
  image = np.asarray(image)
  # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
  input_tensor = tf.convert_to_tensor(image)
  # The model expects a batch of images, so add an axis with `tf.newaxis`.
  input_tensor = input_tensor[tf.newaxis,...]

  # Run inference
  model_fn = model.signatures['serving_default']
  output_dict = model_fn(input_tensor)

  # All outputs are batches tensors.
  # Convert to numpy arrays, and take index [0] to remove the batch dimension.
  # We're only interested in the first num_detections.
  num_detections = int(output_dict.pop('num_detections'))
  output_dict = {key:value[0, :num_detections].numpy() 
                 for key,value in output_dict.items()}
  output_dict['num_detections'] = num_detections

  # detection_classes should be ints.
  output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
   
  # Handle models with masks:
  if 'detection_masks' in output_dict:
    # Reframe the the bbox mask to the image size.
    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
              output_dict['detection_masks'], output_dict['detection_boxes'],
               image.shape[0], image.shape[1])      
    detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                       tf.uint8)
    output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
    
  return output_dict

def show_frame(model,labels,text,label_detect,tb_trans,window,cb,op,btn,src=0):
    cap = cv2.VideoCapture(src)
    thread_inf = Thread(target=update_text,args=(cap,model,labels,text,label_detect,tb_trans,cb,op,btn,))
    thread_inf.start()
    window.protocol("WM_DELETE_WINDOW",prevent_exit)                                                

def update_text(cap,model,labels,text,label_detect,tb_trans,cb,op,btn):
    counter = 0
    last_detect = ""
    last_insert = ""
    cb.config(state=tk.DISABLED)
    op.config(state=tk.DISABLED)
    btn.config(state=tk.DISABLED)
    now = datetime.now()
    while cap.isOpened() :  
        _, frame = cap.read()
        output_dict = run_inference(model, frame)
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            labels,
            instance_masks=output_dict.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=8)
        frame = cv2.resize(frame, (800, 600))
        if output_dict['detection_scores'] > 0.5 :
            value = output_dict['detection_classes'][0]
            obj = labels.get(value)
            obj_name = obj.get('name')
            label_detect.config(text = "Detected word : {}".format(obj_name))
            if  counter == 5 and obj_name == last_detect:
                if obj_name != last_insert :
                    text.config(text="{} {}".format(text["text"],obj_name))
                    last_insert = obj_name
                    now = datetime.now()
            elif obj_name == last_detect:
                counter = counter + 1
            else :
                counter = 0
                last_detect = obj_name
        cv2.moveWindow(WINNAME, 720,0)
        cv2.imshow(WINNAME,frame)
        if(datetime.now() - now).total_seconds() > 3 and not text["text"] == '':
            now = datetime.now()
            last_insert = ""
            convert_speech(text["text"],tb_trans)
            text.config(text="")
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            btn.config(state=tk.NORMAL)
            if TRANSLATE.get() == 1:
                op.config(state="readonly")
                cb.config(state=tk.NORMAL)
            text.config(text="")
            cv2.destroyAllWindows()
            window.protocol("WM_DELETE_WINDOW",window.destroy)
            break
        elif cv2.getWindowProperty(WINNAME, cv2.WND_PROP_VISIBLE) != 1:
            cap.release()
            btn.config(state=tk.NORMAL)
            if TRANSLATE.get() == 1:
                op.config(state="readonly")
                cb.config(state=tk.NORMAL)
            text.config(text="")
            cv2.destroyAllWindows()
            window.protocol("WM_DELETE_WINDOW",window.destroy)
            break

def enable_options(option):
    if TRANSLATE.get() == 1:
        option.config(state="readonly")
    elif TRANSLATE.get() == 0:
        option.config(state=tk.DISABLED)

def check_voice(lbl):
    key = LANGUAGES[CHOSEN_LANGUAGE.get()]
    voices = engine.getProperty('voices')
    voice_found = False
    for voice in voices:
        vid = voice.id
        token = vid.find('TTS')
        tts_lang = vid[token:len(vid)]
        if key in tts_lang.lower():
            engine.setProperty('voice',voice.id)
            engine.setProperty('rate',125)
            voice_found = True
            lbl['text'] = ""
            break
    if voice_found == False:
        reset_voice(1)
        lbl['text'] = "Speech pack for selected language not found!"

def reset_voice(sub=0):
    if TRANSLATE.get() == 0 or sub == 1:
        voices = engine.getProperty('voices')
        for voice in voices:
            vid = voice.id
            token = vid.find('TTS')
            tts_en = vid[token:len(vid)]
            if 'en' in tts_en.lower():
                engine.setProperty('voice',voice.id)
                break

window.geometry("{}x{}+0+0".format(WIDTH,HEIGHT))
window.resizable(False,False)


model,labels = load_data()
img_logo = tk.PhotoImage(file=PATH_TO_LOGO)

frame_misc = tk.Frame(master=window,relief=tk.GROOVE,borderwidth=5,width=WIDTH,height=HEIGHT)
frame_misc.place(x=0,y=0,height=HEIGHT,width=WIDTH)
frame_logo = tk.Frame(master=frame_misc,relief=tk.RIDGE,borderwidth=5)
frame_control = tk.Frame(master=frame_misc,relief=tk.RIDGE,borderwidth=5)
label_logo = tk.Label(master=frame_logo,image=img_logo,width=int(WIDTH/4),height=125)
label_detect = tk.Label(master=frame_logo,text="Detected word : ")
label_buffer = tk.Label(master=frame_logo,text="------------------------------------------")
label_result = tk.Label(master=frame_logo,text="Detected sentence")
label_voice = tk.Label(master=frame_control,text=" ",fg="red")
tb_result = tk.Label(master=frame_logo,text="",bg="black",fg="white")
label_trans = tk.Label(master=frame_logo,text="Translated sentence")
tb_trans = tk.Label(master=frame_logo,text="",bg="black",fg="white")
option_lang = ttk.Combobox(master=frame_control,textvariable=CHOSEN_LANGUAGE,value=list(LANGUAGES.keys()))
cb_lang = tk.Checkbutton(master=frame_control, text="Translate", variable=TRANSLATE, onvalue=1, offvalue=0,command=lambda:enable_options(option_lang))
btn_con = tk.Button(master=frame_control,text="Check for WiFi",command=lambda:msg_box(cb_lang,btn_con,option_lang))
btn_start = tk.Button(master=frame_control,text="Start",command=lambda:show_frame(model,labels,tb_result,label_detect,tb_trans,window,cb_lang,option_lang,btn_start))


cb_lang.config(state=tk.DISABLED)
option_lang.config(state=tk.DISABLED)
label_detect["font"] = FONT
tb_result["font"] = FONT
tb_trans["font"] = FONT
label_buffer["font"] = FONT
label_trans["font"] = FONT
label_result["font"] = FONT
btn_start["font"] = FONT
cb_lang["font"] = FONT
btn_con["font"] = FONT

CHOSEN_LANGUAGE.trace("w", lambda *args: check_voice(label_voice))
TRANSLATE.trace("w",lambda *args: reset_voice())
frame_logo.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
frame_control.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
label_logo.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
label_detect.pack(side=tk.TOP,fill=tk.BOTH)
label_buffer.pack(side=tk.TOP,fill=tk.BOTH)
tb_trans.pack(side=tk.BOTTOM,fill=tk.BOTH)
label_trans.pack(side=tk.BOTTOM)
tb_result.pack(side=tk.BOTTOM,fill=tk.BOTH)
label_result.pack(side=tk.BOTTOM)
btn_start.pack(side=tk.TOP,fill=tk.BOTH,pady=5,padx=5)
btn_con.pack(side=tk.TOP,fill=tk.BOTH,pady=5,padx=5)
cb_lang.pack(side=tk.TOP,fill=tk.BOTH,pady=5,padx=5)
option_lang.pack(side=tk.TOP,fill=tk.BOTH,pady=5,padx=5)
label_voice.pack(side=tk.TOP,fill=tk.BOTH,pady=5,padx=5)


window.mainloop()







