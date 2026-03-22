'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-green-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          {/* Header */}
          <motion.div
            className="mb-8"
            animate={{ y: [0, -10, 0] }}
            transition={{ duration: 3, repeat: Infinity }}
          >
            <h1 className="text-6xl md:text-7xl font-black mb-4">
              <span className="gradient-neon bg-clip-text text-transparent">
                CODEXMATRIX
              </span>
            </h1>
            <p className="text-2xl text-cyan-400 font-bold tracking-widest">
              MILITARY AI COMMAND CENTER
            </p>
          </motion.div>

          {/* Description */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="mb-12 max-w-2xl"
          >
            <p className="text-lg text-slate-300 mb-4 leading-relaxed">
              🎯 <span className="text-green-400 font-bold">TACTICAL BENCHMARKING SYSTEM</span>
            </p>
            <ul className="text-slate-400 space-y-2 text-sm md:text-base">
              <li>⚔️ Peer-Review Matrix Operations (M²)</li>
              <li>🚀 Real-Time AI Model Evaluation</li>
              <li>📡 Live Heatmap & Performance Analysis</li>
              <li>🔐 Privacy-First Architecture</li>
            </ul>
          </motion.div>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <Link href="/benchmark">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="gradient-button px-8 py-4 rounded-lg font-bold text-lg tracking-wider glow-neon hover:shadow-xl transition-all"
              >
                🚀 START BENCHMARK
              </motion.button>
            </Link>
            
            <Link href="/guide">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 rounded-lg font-bold text-lg tracking-wider border-2 border-green-400 text-green-400 hover:bg-green-400 hover:text-slate-950 transition-all"
              >
                📚 VIEW GUIDE
              </motion.button>
            </Link>
          </motion.div>

          {/* Status badge */}
          <motion.div
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="mt-12 inline-flex items-center gap-2 px-4 py-2 bg-slate-800 border border-green-400 rounded-full"
          >
            <span className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></span>
            <span className="text-green-400 font-bold">SYSTEM ONLINE</span>
          </motion.div>
        </motion.div>
      </div>
    </main>
  )
}
