// CustomizationPanel.tsx
import React,{useState} from "react";
import { useTheme } from "./ThemeContext";
import "./styles.css";

const CustomizationPanel: React.FC = () => {
  const { theme, setTheme } = useTheme();
  const [showBubble, setShowBubble] = useState(false);

  const handleFontChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setTheme((prev) => ({ ...prev, fontFamily: event.target.value }));
  };

  return (
    <>
       <div className={`customization-bubble ${showBubble ? 'show-bubble' : ''}`}>
       <label>
          <b>Background Color:</b>
          <input
            type="color"
            value={theme.backgroundColor}
            onChange={(e) =>
              setTheme((prev) => ({ ...prev, backgroundColor: e.target.value }))
            }
          />
        </label>
        <br/>
        <label>
        <b>Background Image:</b>
          <input
            type="file"
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                const url = URL.createObjectURL(e.target.files[0]);
                setTheme((prev) => ({ ...prev, backgroundImage: url }));
              }
            }}
          />
        </label>
        <br/>

       <label> <b>Chat Panel Color:</b></label>
        <label>
        <b> Gradient Start:</b>
          <input
            type="color"
            onChange={(e) =>
              setTheme((prev) => ({ ...prev, gradientStart: e.target.value }))
            }
          />
        </label>
        <br/>

        <label>
        <b>  Gradient End:</b>
          <input
            type="color"
            onChange={(e) =>
              setTheme((prev) => ({ ...prev, gradientEnd: e.target.value }))
            }
          />
        </label>
        <br/>
        <label>
        <b>Font:</b>
          <select value={theme.fontFamily} onChange={handleFontChange}>
            <option value="Arial, sans-serif">Arial</option>
            <option value="'Courier New', Courier, monospace">
              Courier New
            </option>
            <option value="'Georgia', serif">Georgia</option>
            <option value="'Times New Roman', Times, serif">
              Times New Roman
            </option>
            <option value="'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif">
              Trebuchet MS
            </option>
            {/* Add more fonts as desired */}
          </select>
        </label>
        <br/>
        <label>
        <b> Choose Avatar:</b>
          <input
            type="file"
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                const url = URL.createObjectURL(e.target.files[0]);
                setTheme((prev) => ({ ...prev, avatar: url }));
              }
            }}
          />
        </label>
      </div>
      <div onClick={() => setShowBubble(!showBubble)} className={`flex items-center justify-center text-white px-2 py-2 flex-shrink-0 rounded-full cursor-pointer bg-violet-900 hover:bg-violet-950`}>
                <svg fill={" linear-gradient(to right, blue , black)"} xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512">
                  <path d="M448 256c0-106-86-192-192-192V448c106 0 192-86 192-192zM0 256a256 256 0 1 1 512 0A256 256 0 1 1 0 256z"/>
                </svg>
              </div> 
      {/* <button
        className="bubble-toggle-button"
        onClick={() => setShowBubble(!showBubble)}
      >
        Customize Chatbot
      </button> */}
    </>
  );
};

export default CustomizationPanel;
