import React, { useState } from "react";
import Messages from "./components/Messages";
import Field from "./components/Field";
import Img from "./components/Img";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRobot } from "@fortawesome/free-solid-svg-icons";


interface Chat {
  role: "user" | "bot";
  value: string;
  file?: File | null;
}

function App() {
  // Define the initial state for chats
  const [chats, setChats] = useState<Chat[]>([]);

  return (
    <div className="w-screen h-screen py-5 px-20">
      <div className="w-full h-full bg-[#0b1013] rounded-2xl p-5 pt-2 flex flex-col justify-end">
        <div className="text-[#ffae00] p-2 flex flex-row items-center">
          <FontAwesomeIcon className="p-3 bg-[#1f2830] rounded-full mr-2" icon={faRobot} style={{ color: "#ffae00" }} />
          ImageBot
        </div>
        <div className="overflow-y-auto flex-grow justify-end mb-4 px-5">
          {/* Map over the chats and render Messages component dynamically */}
          {chats.map((chat, index) => (
            <React.Fragment key={index}>
              {chat.file && (
                <Img
                  role={chat.role} // You can set the role as needed
                  value={chat.file} // Use the file name as the value
                />
              )}
              {chat.value && <Messages role={chat.role} value={chat.value} />}
            </React.Fragment>
          ))}
        </div>
        <Field setChats={setChats} />
      </div>
    </div>
  );
}

export default App;
