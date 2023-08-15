import { useState, useRef, useEffect } from "react";
import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "../App.css";
import { useTheme } from "./ThemeContext";
import CustomizationPanel from "./CustomizationPanel";
import axios from "axios";
import FileBase64 from "react-file-base64";

type Message = {
  content: string;
  role: "user" | "assistant";
};

function ChatMessage(props: { message: Message }) {
  const { theme } = useTheme();
  if (props.message.role === "assistant") {
    return (
      <div className="col-start-1 col-end-8 p-3 rounded-lg">
        <div className="flex flex-row items-center">
          <div className="flex items-center justify-center h-10 w-10 rounded-full bg-indigo-500 flex-shrink-0">
            A
          </div>
          <div className="relative ml-3 text-sm bg-white py-2 px-4 shadow rounded-xl text-left">
            <ReactMarkdown className="prose" remarkPlugins={[remarkGfm]}>
              {props.message.content}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    );
  } else if (
    props.message.role === "user" &&
    theme.avatar != ""
  ) {
    return (
      <div className="col-start-6 col-end-13 p-3 rounded-lg">
        <div className="flex items-center justify-start flex-row-reverse">
          <div className="flex items-center justify-center h-10 w-10 rounded-full  flex-shrink-0">
            <img
              className=" rounded-md"
              src={theme.avatar}
              alt="Chatbot avatar"
            />
          </div>
          <div className="relative mr-3 text-sm bg-indigo-100 py-2 px-4 shadow rounded-xl text-left">
            <div className="prose">{props.message.content}</div>
          </div>
        </div>
      </div>
    );
  } else if (props.message.role === "user") {
    return (
      <div className="col-start-6 col-end-13 p-3 rounded-lg">
        <div className="flex items-center justify-start flex-row-reverse">
          <div className="flex items-center justify-center h-10 w-10 rounded-full bg-purple-500 flex-shrink-0">
            U
          </div>
          <div className="relative mr-3 text-sm bg-indigo-100 py-2 px-4 shadow rounded-xl text-left">
            <div className="prose">{props.message.content}</div>
          </div>
        </div>
      </div>
    );
  }
}

function ChatBot() {
  const [input, setInput] = useState<string>("");
  const [botState, setBotState] = useState<object>({});
  const [history, setHistory] = useState<Message[]>([
    // {
    //   content: "Hello!",
    //   role: "user",
    // },
    // {
    //   content: "Hey, how may I assist you?",
    //   role: "assistant",
    // },
  ]);
  const [darkMode, setDarkMode] = useState<boolean>(false);

  const chatEndRef = useRef<HTMLDivElement>(null);
  const { theme,setTheme  } = useTheme();
  const chatbotStyles = {
    backgroundColor: theme.backgroundColor,
    foreground: `linear-gradient(45deg, ${theme.gradientStart}, ${theme.gradientEnd})`,
    fontFamily: theme.fontFamily,
    backgroundImage: `url(${theme.backgroundImage})`,
    // ... Other styles
  };
  const toggleTheme = () => {
    if (theme.backgroundColor === '#ffffff') { // This checks if the theme is light
      setTheme({
        ...theme,
        backgroundColor: 'rgb(15 23 42)',
        foregroundColor: 'rgb(3 7 18)',
        gradientStart: 'rgb(3 7 18)',
        gradientEnd: 'rgb(3 7 18)',
        // ... update other properties as necessary for dark mode
      });
      setDarkMode(true)
    } else {
      setTheme({
        ...theme,
        backgroundColor: '#ffffff',
        foregroundColor: 'grey',
        gradientStart: 'rgb(243 244 246)',
        gradientEnd: ' rgb(243 244 246)',
        // ... update other properties as necessary for light mode
      });
      setDarkMode(false)
    }
  };
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [history]);

  async function chatRequest(history: Message[], botState: object) {
    try {
      const response = await fetch("http://localhost:4000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages: history, state: botState }),
      });
      const content: { botResponse: Message; newState: object } =
        await response.json();
      console.log(content);
      setHistory([...history, content.botResponse]);
      setBotState(content.newState);
    } catch (error) {
      console.error("Failed to send chat history:", error);
    }
  }

  function chatInputHandler() {
    if (!input) {
      return;
    }
    const newMessage: Message = {
      content: input,
      role: "user",
    };
    setHistory([...history, newMessage]);
    setInput("");
    chatRequest([...history, newMessage], botState);
  }

  
// Check for browser-specific implementations
const SpeechRecognitionAPI = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;


const [isRecording, setIsRecording] = useState(false);


const recognitionRef = useRef<null | typeof SpeechRecognitionAPI>(null);
const timeoutIdRef = useRef<null | number>(null);

const startRecording = () => {
  if (!SpeechRecognitionAPI) {
    console.error('Speech Recognition API is not supported in this browser.');
    return;
  }
  
  setIsRecording(true);

  recognitionRef.current = new SpeechRecognitionAPI();
  recognitionRef.current.continuous = true;
  recognitionRef.current.interimResults = true;
  recognitionRef.current.lang = "en-US";

  recognitionRef.current.onstart = () => {
    if (timeoutIdRef.current) {
      clearTimeout(timeoutIdRef.current);
    }
  };

  recognitionRef.current.onresult = (event:any) => {
    const results = event.results;
    const lastResultIndex = results.length - 1;
    const transcript = results[lastResultIndex][0].transcript;

    if (timeoutIdRef.current) {
      clearTimeout(timeoutIdRef.current);
    }

    timeoutIdRef.current = setTimeout(() => {
      console.log(transcript);
      sendTranscriptToServer(transcript);
    }, 1200);
  };

  recognitionRef.current.start();
};

const stopRecording = () => {
  setIsRecording(false);
  recognitionRef.current?.stop();

  if (timeoutIdRef.current) {
    clearTimeout(timeoutIdRef.current);
  }
};

  const sendTranscriptToServer = (transcript:string) => {
    console.log(transcript);
    const newMessage: Message = {
      content: transcript,
      role: "user",
    };
    setHistory([...history, newMessage]);
    setInput("");
    chatRequest([...history, newMessage], botState);
  };

  const [inputData, setInputData] = useState({ selectedFile: "" });

  const handleUpload = async () => {
    if (!inputData.selectedFile) return;
    //console.log(inputData.selectedFile);

    try {
      // Assuming Textbase provides an API endpoint to process images
      const encodedParams = new URLSearchParams();
      encodedParams.set("data", inputData.selectedFile);
      encodedParams.set("lang", "eng");
      const options = {
        method: "POST",
        url: "https://ocr-100-image-text-extractor.p.rapidapi.com/ocr",
        headers: {
          "content-type": "application/x-www-form-urlencoded",
          "X-RapidAPI-Key": import.meta.env.VITE_RAPIDAPI_KEY,
          "X-RapidAPI-Host": import.meta.env.VITE_RAPIDAPI_HOST,
        },
        data: encodedParams,
      };

      try {
        const response = await axios.request(options);
        console.log(response.data);
        const newMessage: Message = {
            content: response.data,
            role: "user",
          };
        setHistory([...history, newMessage]);
        setInputData({selectedFile:''})
        chatRequest([...history, newMessage], botState);
      } catch (error) {
        console.error(error);
      }

    } catch (error) {
      console.error("Error uploading image:", error);
    }
  };

  return (
    <div
      style={chatbotStyles}
      className={`flex h-screen antialiased text-gray-800 bg-white `}
    >
      <div className="flex flex-row h-full w-full overflow-x-hidden">
        <div className="flex flex-col flex-auto h-full p-6 ">
          <div
            style={{
              background:  chatbotStyles.foreground
            }}
            className={`flex flex-col flex-auto flex-shrink-0 rounded-2xl h-full p-4 `}
            
            
            
          >
            <div
            
            className="flex flex-col h-full overflow-x-auto mb-4">
              <div className="grid grid-cols-12 gap-y-2">
                {history.map((message, idx) => (
                  <ChatMessage message={message} key={idx} />
                ))}
                <div ref={chatEndRef}></div>
              </div>
            </div>
            <div
              className={`flex flex-row gap-0.5 items-center h-16 rounded-xl w-full px-4  ${darkMode ? "bg-gray-950" : "bg-white"}`}
            >
               <div onClick={toggleTheme} className={`flex items-center justify-center text-white px-2 py-2 flex-shrink-0 rounded-full cursor-pointer ${darkMode ? "bg-white hover:bg-yellow-50" : "bg-violet-900 hover:bg-violet-950"}`}>
                <svg fill={darkMode ? "rgb(76,29,149)":"white"} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512">
                  <path d="M448 256c0-106-86-192-192-192V448c106 0 192-86 192-192zM0 256a256 256 0 1 1 512 0A256 256 0 1 1 0 256z"/>
                </svg>
              </div>
              <CustomizationPanel />

              <div className="flex-grow ml-2">
                <div className="relative w-full">
                  <input
                    type="text"
                    className={`flex w-full border rounded-xl focus:outline-none focus:border-indigo-300 pl-4 h-10  ${darkMode ? "bg-gray-800 text-white border-none" : "bg-white"}`}
                    value={input}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                      setInput(e.target.value);
                    }}
                    onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
                      if (e.key === "Enter") {
                        chatInputHandler();
                      }
                    }}
                  />
                </div>
              </div>
              <div>
               
               
            
              </div>
              <div className="flex ml-4">
              <FileBase64
                  type="file"
                  multiple={false}
                  onDone={({ base64 }: { base64: string }) =>
                    setInputData({ ...inputData, selectedFile: base64 })
                  }
                />
               {!inputData.selectedFile ? (<>
                <button
                  className="flex items-center justify-center bg-indigo-500 hover:bg-indigo-600 rounded-xl text-white px-4 py-1 flex-shrink-0"
                  onClick={() => {
                    chatInputHandler();
                  }}
                >
                  <span>Send</span>
                  <span className="ml-2">
                    <svg
                      className="w-4 h-4 transform rotate-45 -mt-px"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                      ></path>
                    </svg>
                  </span>
                </button>
               </>)
               :
               (<> <button
                className="flex items-center justify-center bg-indigo-500 hover:bg-indigo-600 rounded-xl text-white px-4 py-1 flex-shrink-0"
                 onClick={handleUpload}>Upload Image</button></>)

               }
              </div>
              <div className="ml-4">
                <button
                  className="flex items-center justify-center bg-indigo-500 hover:bg-indigo-600 rounded-xl text-white px-4 py-1 flex-shrink-0"
                  onClick={isRecording ? stopRecording : startRecording}
                >
                  {isRecording ? "Stop Recording" : "Start Recording"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatBot;
