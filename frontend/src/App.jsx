import { useState } from "react"

function App() {
  const [question, setQuestion] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAsk = async () => {
    if (!question.trim()) return
    setLoading(true)
    setResult(null)
    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question }),
      })
      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error("Request failed:", error)
    }
    setLoading(false)
  }

  const statusStyles = {
    Supported: "bg-green-500/10 text-green-400 border-green-500/30",
    Contradicted: "bg-red-500/10 text-red-400 border-red-500/30",
    Unverified: "bg-yellow-500/10 text-yellow-400 border-yellow-500/30",
    Unverifiable: "bg-yellow-500/10 text-yellow-400 border-yellow-500/30",
  }

  return (
    <div className="min-h-screen bg-black text-gray-100 font-sans">
      <div className="max-w-3xl mx-auto px-6 py-16">

        <h1 className="text-4xl font-semibold tracking-tight mb-2 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
          TrustRAG
        </h1>
        <p className="text-gray-500 mb-10">
          Ask a question. Every claim gets verified against the source.
        </p>

        <div className="flex gap-3 mb-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Ask a question..."
            className="flex-1 bg-gray-900 border border-gray-800 rounded-lg px-4 py-3
                       text-gray-100 placeholder-gray-600 outline-none
                       focus:border-gray-500 transition-colors duration-200"
          />
          <button
            onClick={handleAsk}
            disabled={loading}
            className="bg-white text-black font-medium px-6 py-3 rounded-lg
                       transition-all duration-200 hover:bg-gray-200 hover:scale-[1.02]
                       active:scale-[0.98] disabled:opacity-40 disabled:hover:scale-100"
          >
            {loading ? "..." : "Ask"}
          </button>
        </div>

        {loading && (
          <div className="flex items-center gap-3 text-gray-500 mt-8 animate-pulse">
            <div className="w-4 h-4 border-2 border-gray-600 border-t-white rounded-full animate-spin"></div>
            <span>Retrieving, generating, verifying...</span>
          </div>
        )}

        {result && !loading && (
          <div className="mt-10 animate-[fadeIn_0.4s_ease-out]">
            <div className="flex gap-2 mb-4 text-xs text-gray-600">
              <span className="border border-gray-800 rounded-full px-3 py-1">
                chunk_size: {result.chunk_size}
              </span>
              <span className="border border-gray-800 rounded-full px-3 py-1">
                top_k: {result.top_k}
              </span>
            </div>

            <div className="bg-gray-950 border border-gray-800 rounded-xl p-6 mb-6 leading-relaxed text-gray-200">
              {result.answer}
            </div>

            <h2 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">
              Claim Verification
            </h2>
            <div className="space-y-2">
              {result.claims.map((c, index) => (
                <div
                  key={index}
                  className={`border rounded-lg px-4 py-3 text-sm transition-all duration-200 hover:translate-x-1 ${
                    statusStyles[c.status] || "bg-gray-900 text-gray-400 border-gray-800"
                  }`}
                  style={{ animationDelay: `${index * 60}ms` }}
                >
                  <span className="font-semibold mr-2">{c.status}</span>
                  <span className="text-gray-300">{c.claim}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App