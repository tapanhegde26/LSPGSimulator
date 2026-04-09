export default function MoonVisual() {
  return (
    <div className="flex justify-center items-center mt-6">
      <div className="relative">
        
        {/* Moon */}
        <div className="w-32 h-32 rounded-full bg-gray-300 shadow-inner"></div>

        {/* Solar Ring */}
        <div className="absolute inset-0 rounded-full border-4 border-blue-400 animate-pulse"></div>

      </div>
    </div>
  );
}
