import React from 'react';

const GlassSphere: React.FC = () => {
  return (
    <div className="relative w-96 h-96 flex flex-col items-center justify-center">
      {/* Надпись сверху сферы */}
      <div className="absolute -top-16 left-1/2 transform -translate-x-1/2 text-center">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 bg-clip-text text-transparent font-['Inter',system-ui,-apple-system,sans-serif] tracking-wide">
          AI Бухгалтер
        </h2>
        <p className="text-sm text-gray-400 mt-1 font-['Inter',system-ui,-apple-system,sans-serif] font-medium">
          Умная автоматизация
        </p>
      </div>
      
      {/* Тёмная тень для глубины */}
      <div className="absolute w-80 h-80 rounded-full bg-black/30 blur-3xl"></div>
      
      {/* Основная сфера с градиентом */}
      <div className="absolute w-80 h-80 rounded-full bg-gradient-to-br from-indigo-500/40 via-blue-600/50 to-purple-600/40 backdrop-blur-xl border border-white/20 shadow-2xl animate-pulse">
        
        {/* Внутренний блик */}
        <div className="absolute top-8 left-8 w-24 h-24 rounded-full bg-gradient-to-br from-white/50 to-transparent blur-sm animate-pulse"></div>
        
        {/* Внешний блик */}
        <div className="absolute top-4 left-4 w-32 h-32 rounded-full bg-gradient-to-br from-white/20 to-transparent blur-md animate-pulse"></div>
        
        {/* Внутренняя сфера с данными */}
        <div className="absolute inset-8 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-500/20 border border-white/10" style={{animation: 'spin 20s linear infinite'}}>
          
          {/* Центральный элемент - символ лея */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-4xl font-bold text-blue-300 animate-pulse font-['Inter',system-ui,-apple-system,sans-serif]">₼</div>
          </div>
          
          {/* Вращающиеся кольца с данными */}
          <div className="absolute inset-0 rounded-full border border-blue-300/20" style={{animation: 'spin 15s linear infinite reverse'}}></div>
          <div className="absolute inset-4 rounded-full border border-purple-300/20" style={{animation: 'spin 20s linear infinite'}}></div>
          <div className="absolute inset-8 rounded-full border border-cyan-300/20" style={{animation: 'spin 15s linear infinite reverse'}}></div>
          
          {/* Плавающие цифры и символы */}
          <div className="absolute top-2 left-1/2 transform -translate-x-1/2 text-xs text-blue-200 animate-bounce font-['Inter',system-ui,-apple-system,sans-serif] font-semibold">2025</div>
          <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 text-xs text-purple-200 animate-bounce font-['Inter',system-ui,-apple-system,sans-serif] font-semibold">MDL</div>
          <div className="absolute left-2 top-1/2 transform -translate-y-1/2 text-xs text-cyan-200 animate-bounce font-['Inter',system-ui,-apple-system,sans-serif] font-semibold">%</div>
          <div className="absolute right-2 top-1/2 transform -translate-y-1/2 text-xs text-green-200 animate-bounce font-['Inter',system-ui,-apple-system,sans-serif] font-semibold">+</div>
          
          {/* Мерцающие точки как данные */}
          <div className="absolute top-4 left-4 w-1 h-1 bg-blue-300 rounded-full animate-ping"></div>
          <div className="absolute top-6 right-6 w-1 h-1 bg-purple-300 rounded-full animate-ping" style={{animationDelay: '0.5s'}}></div>
          <div className="absolute bottom-4 left-6 w-1 h-1 bg-cyan-300 rounded-full animate-ping" style={{animationDelay: '1s'}}></div>
          <div className="absolute bottom-6 right-4 w-1 h-1 bg-green-300 rounded-full animate-ping" style={{animationDelay: '1.5s'}}></div>
          
          {/* График внутри сферы */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex items-end space-x-1">
            <div className="w-1 bg-blue-300 h-3 animate-pulse"></div>
            <div className="w-1 bg-purple-300 h-5 animate-pulse" style={{animationDelay: '0.2s'}}></div>
            <div className="w-1 bg-cyan-300 h-2 animate-pulse" style={{animationDelay: '0.4s'}}></div>
            <div className="w-1 bg-green-300 h-4 animate-pulse" style={{animationDelay: '0.6s'}}></div>
            <div className="w-1 bg-blue-300 h-6 animate-pulse" style={{animationDelay: '0.8s'}}></div>
          </div>
          
          {/* Вращающиеся сегменты */}
          <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-300/30 border-r-purple-300/30 border-b-cyan-300/30 border-l-green-300/30" style={{animation: 'spin 20s linear infinite'}}></div>
          
        </div>
        
        {/* Внешние кольца */}
        <div className="absolute -inset-4 rounded-full border border-blue-400/10" style={{animation: 'spin 15s linear infinite reverse'}}></div>
        <div className="absolute -inset-8 rounded-full border border-purple-400/10" style={{animation: 'spin 20s linear infinite'}}></div>
        <div className="absolute -inset-12 rounded-full border border-cyan-400/10" style={{animation: 'spin 15s linear infinite reverse'}}></div>
        
        {/* Мерцающие частицы вокруг сферы */}
        <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-blue-300 rounded-full animate-ping"></div>
        <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-purple-300 rounded-full animate-ping" style={{animationDelay: '0.3s'}}></div>
        <div className="absolute left-1/2 -left-2 top-1/2 transform -translate-y-1/2 w-1 h-1 bg-cyan-300 rounded-full animate-ping" style={{animationDelay: '0.6s'}}></div>
        <div className="absolute left-1/2 -right-2 top-1/2 transform -translate-y-1/2 w-1 h-1 bg-green-300 rounded-full animate-ping" style={{animationDelay: '0.9s'}}></div>
        
        {/* Дополнительные блики для 3D эффекта */}
        <div className="absolute top-12 left-12 w-8 h-8 rounded-full bg-gradient-to-br from-white/30 to-transparent blur-sm"></div>
        <div className="absolute bottom-12 right-12 w-6 h-6 rounded-full bg-gradient-to-br from-white/20 to-transparent blur-sm"></div>
        
      </div>
      
      {/* CSS анимации через style tag */}
      <style dangerouslySetInnerHTML={{
        __html: `
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `
      }} />
    </div>
  );
};

export default GlassSphere; 