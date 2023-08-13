import React from 'react';
import { BotProps, ChatWindow } from '../index';

const FullPageBot: React.FC<BotProps> = (props) => {
    return (
        <ChatWindow windowHeight={'h-screen'} windowWidth={''} corners={''} {...props}/>
    );
}


export default FullPageBot;