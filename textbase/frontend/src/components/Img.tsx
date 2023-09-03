import React from "react";

const Img = ({ value, role }) => {
  return (
    <div
      className={`flex my-3 ${role == "user" && "justify-end"} ${
        role == "bot" && "justify-start"
      }`}
    >
      <div
        className={`${role == "user" && "bg-[#ffae00] text-black"} ${
          role == "bot" && "bg-[#2e3c47] text-white"
        } rounded-lg p-2 max-w-[70%]`}
      >
        <a
          href={URL.createObjectURL(value)}
          download={value.name} // Set the download attribute with the file name
        >
          <img
            src={URL.createObjectURL(value)}
            alt={value.name}
            className="w-80 h-50 cursor-pointer" 
          />
        </a>
      </div>
    </div>
  );
};

export default Img;
