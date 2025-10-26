export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">GEO Optimizer</h2>
              <p className="text-xs text-gray-500">Generative Engine Optimization</p>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">
              Dashboard
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">
              Analytics
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">
              Settings
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
}

