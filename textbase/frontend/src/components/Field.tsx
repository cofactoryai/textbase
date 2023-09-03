import React, { useRef, useState, ChangeEvent, FormEvent } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPlus,
  faPaperPlane,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import Lottie from "lottie-react";
import Typing from "../assets/Typing.json";
import Tesseract from "tesseract.js";
import axios from "axios";

interface FileCard {
  file: File;
  id: number;
}

interface Chat {
  role: "user" | "bot";
  value: string;
  file?: File | null;
}

const Field: React.FC = ({ setChats }) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [active, setActive] = useState<boolean>(true);
  const [selectedFiles, setSelectedFiles] = useState<FileCard[]>([]);
  const [textInput, setTextInput] = useState<string>("");

  const handleFileUpload = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const files = Array.from(e.target.files);
    const allowedFileTypes = [".png", ".jpg", ".jpeg"];
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

  const ImageToTextConvert = (imagefile: File) => {
    return new Promise((resolve, reject) => {
      Tesseract.recognize(imagefile, "eng", {})
        .catch((err) => {
          console.error(err);
          reject(err); // Reject the promise if there's an error
        })
        .then((result) => {
          const recognizedText = result?.data.text || "";
          console.log(recognizedText);
          resolve(recognizedText); // Resolve the promise with the recognized text
        });
    });
  };

  const handleFileInputClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleTextInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setTextInput(e.target.value);
  };

  const textquery = async (data: String) => {
    try {
      const response = await fetch(
        "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
        {
          method: "POST",
          headers: {
            Authorization: "Bearer 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",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const blob = await response.blob();
      const fileName = "bot_response.png";
      const file = new File([blob], fileName, { type: blob.type });
      return file;
    } catch (error) {
      console.error("Error querying the API:", error);
      throw error;
    }
  };

  const imagequery = async (imagefile: File) => {
    try {
      const apiUrl =
        "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large";
      const headers = {
        Authorization: "Bearer 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",
        "Content-Type": "application/octet-stream", // Set content type to binary
      };
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: headers,
        body: imagefile,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const result = await response.json();
      return result[0].generated_text;
    } catch (error) {
      console.error("Error querying the API:", error);
      throw error;
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    setActive(false);
    e.preventDefault();
    console.log("Text Input:", textInput);
    console.log(
      "Selected Files:",
      selectedFiles.map((fileCard) => fileCard.file)
    );
    const newChat: Chat = {
      role: "user",
      value: textInput,
      file: selectedFiles.length > 0 ? selectedFiles[0].file : null,
    };
    setChats((prevChats: Chat[]) => [...prevChats, newChat]);
    setTextInput("");
    setSelectedFiles([]);
    let botChat: Chat = { role: "bot", value: "", file: null };
    if (newChat.value !== null && newChat.file === null) {
      const botResponse = await textquery({ inputs: textInput });
      botChat = {
        role: "bot",
        value: "",
        file: botResponse,
      };
    } else if (newChat.value === "" && newChat.file !== null) {
      const botResponse = await imagequery(selectedFiles[0].file);
      botChat = {
        role: "bot",
        value: botResponse,
        file: null,
      };
    } else if (newChat.value !== "" && newChat.file !== null) {
      const botResponse = await ImageToTextConvert(selectedFiles[0].file);
      botChat = {
        role: "bot",
        value: botResponse,
        file: null,
      };
    }
    // const imageText = await ImageToTextConvert(selectedFiles[0].file);

    setActive(true);
    setChats((prevChats: Chat[]) => [...prevChats, botChat]);
  };

  return (
    <div>
      {!active && (
        <div className="w-24 h-10 absolute bottom-[140px] left-[110px]">
          <Lottie loop={true} animationData={Typing} />
        </div>
      )}
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
              <FontAwesomeIcon
                icon={faPlus}
                size="xl"
                style={{ color: "#ffae00" }}
              />
            </button>
            <button
              disabled={!active}
              className="mx-2 px-4 py-2 rounded-xl hover:bg-[#1f2830]"
              type="submit"
            >
              <FontAwesomeIcon
                icon={faPaperPlane}
                size="xl"
                style={{ color: active ? "#ffae00" : "#2e3c47" }}
              />
            </button>
          </div>
        </div>
        <div className="flex flex-row flex-wrap  mx-5">
          {selectedFiles.map((fileCard) => (
            <div
              key={fileCard.id}
              className="bg-gray-800 rounded-xl p-2 mt-2 mx-1 flex flex-row items-center text-white"
            >
              <img
                src={URL.createObjectURL(fileCard.file)} // Create an object URL for the image
                alt={fileCard.file.name}
                className="w-20 h-10"
              />
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
