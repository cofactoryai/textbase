import React, { useRef, useState, ChangeEvent, FormEvent } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus, faPaperPlane,faXmark } from "@fortawesome/free-solid-svg-icons";

interface FileCard {
  file: File;
  id: number;
}

interface Chat {
  role: "user" | "bot";
  value: string;
  file?: File | null;
}

const Field: React.FC = ({setChats}) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFiles, setSelectedFiles] = useState<FileCard[]>([]);
  const [textInput, setTextInput] = useState<string>("");

  const handleFileUpload = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const files = Array.from(e.target.files);

    // Filter files to include only specific types
    const allowedFileTypes = [".png", ".jpg", ".jpeg", ".csv", ".pdf"];
    const validFiles = files.filter((file) =>
      allowedFileTypes.includes(file.name.slice(file.name.lastIndexOf(".")))
    );

    const fileCards = validFiles.map((file, index) => ({
      file,
      id: index,
    }));

    setSelectedFiles([...selectedFiles, ...fileCards]);
  };

  const handleRemoveFile = (id: number) => {	
    const updatedFiles = selectedFiles.filter((fileCard) => fileCard.id !== id);	
    setSelectedFiles(updatedFiles);	
  };

  const handleFileInputClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleTextInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setTextInput(e.target.value);
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    // Handle the text input value (textInput) and selected files (selectedFiles) here
    console.log("Text Input:", textInput);
    console.log("Selected Files:", selectedFiles.map((fileCard) => fileCard.file));
    const newChat: Chat = {
      role: "user",
      value: textInput,
      file: selectedFiles.length > 0 ? selectedFiles[0].file : null,
    };    
  
    
    // Append the new chat message to the existing chats
    setChats((prevChats: Chat[]) => [...prevChats, newChat]);

    // Clear the text input and selected files after handling
    setTextInput("");
    setSelectedFiles([]);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="bg-[#141a1f] rounded-lg flex flex-row items-center p-1 mx-5">
          <input
            type="file"
            accept=".png, .jpg, .jpeg, .csv, .pdf"
            ref={fileInputRef}
            style={{ display: "none" }}
            onChange={handleFileUpload}
            multiple
          />
          <input
            className="bg-transparent p-3 rounded-xl text-white flex-grow outline-none"
            placeholder="Write a message....."
            type="text"
            value={textInput}
            onChange={handleTextInputChange}
          />
          <div className="flex">
            <button
              className="px-4 py-2 rounded-xl hover:bg-[#1f2830]"
              onClick={handleFileInputClick}
              type="button"
            >
              <FontAwesomeIcon icon={faPlus} size="xl" style={{ color: "#ffae00" }} />
            </button>
            <button className="mx-2 px-4 py-2 rounded-xl hover:bg-[#1f2830]" type="submit">
              <FontAwesomeIcon
                icon={faPaperPlane}
                size="xl"
                style={{ color: "#ffae00" }}
              />
            </button>
          </div>
        </div>
        <div className="flex flex-row flex-wrap  mx-5">
          {selectedFiles.map((fileCard) => (
            <div key={fileCard.id} className="bg-gray-800 rounded-xl p-2 mt-2 mx-1 text-white">
              {fileCard.file.name}
              <button	
                className="text-red-500 hover:text-red-700 ml-2"	
                onClick={() => handleRemoveFile(fileCard.id)}	
              >	
                <FontAwesomeIcon icon={faXmark} />	
              </button>
            </div>
          ))}
        </div>
      </form>
    </div>
  );
};

export default Field;
