export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center space-y-4">
      <div className="relative w-20 h-20">
        <div className="absolute top-0 left-0 w-full h-full">
          <div className="w-20 h-20 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
        </div>
      </div>
      <div className="text-center">
        <p className="text-lg font-medium text-gray-900">Analyzing website...</p>
        <p className="text-sm text-gray-500 mt-1">This may take a few seconds</p>
      </div>
    </div>
  );
}

