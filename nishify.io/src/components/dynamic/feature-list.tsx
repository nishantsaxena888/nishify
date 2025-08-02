'use client'

import React from 'react'

type Feature = {
  title: string
  description: string
}

type Props = {
  title?: string
  features?: Feature[]
}

const FeatureList: React.FC<Props> = ({ title = 'Features', features = [] }) => {
  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-bold">{title}</h2>
      <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {features.map((feat, idx) => (
          <li key={idx} className="border rounded-lg p-4 shadow-sm">
            <h3 className="font-semibold">{feat.title}</h3>
            <p className="text-sm text-muted-foreground">{feat.description}</p>
          </li>
        ))}
      </ul>
    </section>
  )
}

export default FeatureList
