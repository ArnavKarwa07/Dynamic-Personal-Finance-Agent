/**
 * CSS Diagnostic Component
 * Test component to verify Tailwind CSS is working
 */
import React from "react";

const CSSTest = () => {
  return (
    <div className="fixed top-4 left-4 z-50 bg-red-500 text-white p-4 rounded-lg shadow-lg">
      <h3 className="font-bold text-lg">CSS Test</h3>
      <p className="text-sm">If you see styled red box, Tailwind is working!</p>
      <div className="mt-2 flex space-x-2">
        <div className="w-4 h-4 bg-blue-500 rounded"></div>
        <div className="w-4 h-4 bg-green-500 rounded"></div>
        <div className="w-4 h-4 bg-yellow-500 rounded"></div>
      </div>
    </div>
  );
};

export default CSSTest;
