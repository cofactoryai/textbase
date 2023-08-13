import React from 'react';
import {
    BotProps, ChatWindow,
} from '../index';

/**
 * Implements an out of the box flaoting chat window with a FAB toggle.
 * @param props {@link BotProps}
 * @returns 
 */
const FloatingWindowBot: React.FC<BotProps> = (props) => {
    const [chatWindow, setChatWindow] = React.useState<boolean>(false);

    const toggleChatWindow = () => {
        setChatWindow(!chatWindow);
    }

    return <>
        <div className='fixed bottom-10 right-10'>
            {chatWindow &&
                <div className='rounded-lg shadow-lg'>
                    <ChatWindow {...props} windowHeight='h-1/2' windowWidth='' corners='rounded-lg'/>
                </div>
            }
        </div>
        <div className="fixed bottom-4 right-4">
            {
                !chatWindow ?
                    <button onClick={toggleChatWindow} id="chatToggle" className="bg-indigo-500 hover:bg-indigo-600 text-white rounded-full p-4 shadow-lg">
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                        </svg>
                    </button> :
                    <button onClick={toggleChatWindow} id="chatToggle" className="bg-indigo-500 hover:bg-indigo-600 text-white rounded-full p-4 shadow-lg">
                        {
                            chatWindow &&
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        }
                    </button>
            }
        </div>

    </>
}


export default FloatingWindowBot;