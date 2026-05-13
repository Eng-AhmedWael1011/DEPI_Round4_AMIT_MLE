export default function SentimentApp() {
  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center p-6">
      <div className="w-full max-w-2xl bg-white rounded-3xl shadow-xl p-8">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-slate-800 mb-2">
            Sentiment Analysis API
          </h1>

          <p className="text-slate-500 text-lg">
            FastAPI + NLP Inference Pipeline
          </p>
        </div>

        <SentimentForm />
      </div>
    </div>
  )
}

import { useState } from "react"

function SentimentForm() {

  const [review, setReview] = useState("")

  const [result, setResult] = useState(null)

  const [loading, setLoading] = useState(false)

  const [error, setError] = useState("")


  async function handlePrediction() {

    if (!review.trim()) {
      setError("Please enter a review")
      return
    }

    setLoading(true)
    setError("")

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            review: review
          })
        }
      )

      const data = await response.json()

      setResult(data)

    } catch {

      setError("Failed to connect to FastAPI server")

    } finally {

      setLoading(false)
    }
  }


  return (
    <div>

      <textarea
        rows={8}
        placeholder="Enter your movie review here..."
        value={review}
        onChange={(e) => setReview(e.target.value)}
        className="w-full border border-slate-300 rounded-2xl p-4 text-lg focus:outline-none focus:ring-2 focus:ring-slate-400 resize-none"
      />


      <button
        onClick={handlePrediction}
        disabled={loading}
        className="w-full mt-4 bg-slate-800 text-white py-4 rounded-2xl text-lg font-semibold hover:bg-slate-700 transition-all disabled:opacity-50"
      >
        {
          loading
            ? "Analyzing Review..."
            : "Predict Sentiment"
        }
      </button>


      {
        error && (
          <div className="mt-4 bg-red-100 text-red-700 p-4 rounded-2xl">
            {error}
          </div>
        )
      }


      {
        result && (
          <div className="mt-6 border border-slate-200 rounded-3xl p-6 bg-slate-50">

            <h2 className="text-2xl font-bold text-slate-800 mb-4">
              Prediction Result
            </h2>

            <div className="space-y-3 text-lg">

              <div className="flex justify-between">
                <span className="font-semibold text-slate-600">
                  Sentiment
                </span>

                <span
                  className={`font-bold ${
                    result.sentiment === "Positive"
                      ? "text-green-600"
                      : "text-red-600"
                  }`}
                >
                  {result.sentiment}
                </span>
              </div>


              <div className="flex justify-between">
                <span className="font-semibold text-slate-600">
                  Confidence
                </span>

                <span className="font-bold text-slate-800">
                  {(result.confidence * 100).toFixed(2)}%
                </span>
              </div>

            </div>

          </div>
        )
      }

    </div>
  )
}
