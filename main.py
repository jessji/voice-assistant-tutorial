import openai
import speech_recognition as sr
from gtts import gTTS
import os
# import pyttsx3
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY # 替换为你的OpenAI API Key

def get_response(prompt):
    # role_description = "你是我的助手和好朋友，你性格积极乐观，说话俏皮可爱，简洁明了。"
    role_description = "你是我的英文老师，你会帮我纠正我的发音、语法和表达错误。"
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {"role": "system", "content": role_description}, # 设定AI的角色，也可以不设定
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

# 文字转语音
def speak(text):
    # 方式1: 使用gtts实现文字转语音
    # tts = gTTS(text, lang='zh-cn')  # 设置语言为中文
    tts = gTTS(text, lang='en')  # 设置语言为英文
    tts.save("output.mp3")
    os.system("afplay output.mp3")  # 适用于 macOS

    # # 方式2: 使用pyttsx3实现文字转语音（无法识别中文）
    # engine = pyttsx3.init()
    # engine.setProperty('rate', 180)  # 调整语速
    # engine.say(text)
    # engine.runAndWait()

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("语音助手已启动！")

    while True:
        print("请说话...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # user_input = recognizer.recognize_google(audio, language="zh-CN") # 识别语言：中文为"zh-CN"，英文为"en-US"
            user_input = recognizer.recognize_google(audio, language="en-US") # 识别语言：中文为"zh-CN"，英文为"en-US"
            print("你说：", user_input)

            prompt = "用户说：" + user_input + "\n助手回答："
            response = get_response(prompt)
            print("助手：", response)
            speak(response)  # 让语音助手通过语音回答

        except sr.UnknownValueError:
            print("抱歉，我无法识别你说的话。")
        except sr.RequestError:
            print("无法连接到语音识别服务。")

if __name__ == "__main__":
    main()