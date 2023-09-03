import React, { useState } from "react";
import Messages from "./components/Messages";
import Field from "./components/Field";

interface Chat {
  role: "user" | "bot";
  value: string;
  file?: File | null;
}

function App() {
  // Define the initial state for chats
  const [chats, setChats] = useState<Chat[]>([]);

  return (
    <div className="w-screen h-screen py-10 px-20">
      <div className="w-full h-full bg-[#0b1013] rounded-2xl p-5 flex flex-col justify-end">
        <div className="overflow-y-auto mb-4 px-5">
          {/* Map over the chats and render Messages component dynamically */}
          {chats.map((chat, index) => (
            <React.Fragment key={index}>
              {chat.file && (
                <Messages
                  role="user" // You can set the role as needed
                  value={chat.file?.name} // Use the file name as the value
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
