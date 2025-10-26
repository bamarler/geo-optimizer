import { useState } from 'react';

export default function BrandDescription({ initialDescription, onApprove, websiteTitle }) {
  const [description, setDescription] = useState(initialDescription);
  const [isEditing, setIsEditing] = useState(false);

  const handleApprove = () => {
    onApprove(description);
  };

  const wordCount = description.split(/\s+/).filter(word => word.length > 0).length;

  return (
    <div className="card max-w-4xl mx-auto">
      <div className="space-y-6">
        {/* Header */}
        <div className="text-center space-y-3">
          <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-green-700 rounded-full flex items-center justify-center mx-auto">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold text-gray-900">Review Brand Description</h2>
          <p className="text-gray-600">
            AI generated this description for <strong>{websiteTitle}</strong>. Edit if needed or approve to continue.
          </p>
        </div>

        {/* Description Editor */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-gray-700">
              Brand Description
            </label>
            <div className="flex items-center space-x-3">
              <span className="text-xs text-gray-500">{wordCount} words</span>
              <button
                onClick={() => setIsEditing(!isEditing)}
                className="text-sm text-primary-600 hover:text-primary-700 font-medium"
              >
                {isEditing ? 'Preview' : 'Edit'}
              </button>
            </div>
          </div>

          {isEditing ? (
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full h-40 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none resize-none"
              placeholder="Describe what this business does and who it serves..."
            />
          ) : (
            <div className="bg-gray-50 rounded-lg p-6 border-l-4 border-primary-500">
              <p className="text-gray-800 leading-relaxed text-lg">
                {description}
              </p>
            </div>
          )}
        </div>

        {/* Tips */}
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <svg className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="text-sm text-blue-800">
              <p className="font-medium mb-1">💡 Tips for a good description:</p>
              <ul className="space-y-1 list-disc list-inside text-blue-700">
                <li>Keep it concise (3-4 sentences)</li>
                <li>Mention what the business does</li>
                <li>Include who they serve (target audience)</li>
                <li>Highlight unique value or positioning</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-center space-x-4 pt-4">
          <button
            onClick={handleApprove}
            disabled={!description.trim()}
            className="btn-primary"
          >
            <span className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Approve & Continue
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}

