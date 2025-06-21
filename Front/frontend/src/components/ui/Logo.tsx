import React from 'react';

const Logo = () => {
  return (
    <div className="flex items-center gap-2">
      <div className="w-9 h-9 flex items-center justify-center rounded-full bg-white/50 backdrop-blur-sm border border-black/5">
        <svg 
            width="22" 
            height="22" 
            viewBox="0 0 24 24" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg" 
            className="text-primary"
        >
            {/* The two arrows, simplified to one trend */}
            <path d="M7 17L17 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M11 7H17V13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            
            {/* The bars, simplified */}
            <path d="M7 12V17" stroke="currentColor" strokeOpacity="0.6" strokeWidth="2" strokeLinecap="round"/>
            <path d="M12 17V14" stroke="currentColor" strokeOpacity="0.6" strokeWidth="2" strokeLinecap="round"/>
            <path d="M17 17V11" stroke="currentColor" strokeOpacity="0.6" strokeWidth="2" strokeLinecap="round"/>
        </svg>
      </div>
      <span className="text-xl font-bold text-primary">ContaSfera</span>
    </div>
  );
};

export default Logo; 