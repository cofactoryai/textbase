import React from "react";

const Messages = ({ value, role }) => {
  return (
    <div
      className={`flex my-3 ${role == "user" && "justify-end"} ${
        role == "bot" && "justify-start"
      }`}
    >
      <div
        className={`${role == "user" && "bg-[#ffae00] text-black"} ${
          role == "bot" && "bg-[#2e3c47] text-white"
        } rounded-lg p-3 max-w-[70%]`}
      >
        {value}
      </div>
    </div>
  );
};

export default Messages;
