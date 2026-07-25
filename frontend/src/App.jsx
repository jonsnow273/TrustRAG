import { useState } from "react"

function App(){
  const[question, setQuestion] = useState("")
  const[result, setResult] = useState(null)
  const[loading, setLoading] = useState(false)

  const handleAsk = async () => {
    setLoading(true)
    try {
      const response = await fetch("http://127.0.0.1:8000/ask"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: question }),
      })
      const data = await response.json()
      setResult(data)
    } catch (error){
      console.error("Request failed:", error)
    }
    setLoading(false)
  }

  return (
    <div className = "max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-4">TrustRAG</h1>
      <div className="flex gap-2 mb-6">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 border rounded px-3 py-2"
        />
        <button
          onClick={handleAsk}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Ask 
        </button>
    </div>

    {loading && <p>Loading...</p>}

      {result && (
        <div>
          <p className="mb-2 text-sm text-gray-500">
            Config used: chunk_size={result.chunk_size}, top_k={result.top_k}
          </p>

          <p className="mb-4">{result.answer}</p>

          <h2 className="text-lg font-semibold mb-2">Claims</h2>
          <ul className="space-y-2">
            {result.claims.map((c, index) => (
              <li key={index} className="border p-2 rounded">
                <span className="font-medium">{c.status}:</span> {c.claim}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App