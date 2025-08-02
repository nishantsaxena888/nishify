'use client'

import React from 'react'

type Props = {
  title?: string
  subtitle?: string
  backgroundColor?: string
}

const HeroBanner: React.FC<Props> = ({
  title = 'Welcome to Nishify',
  subtitle = 'Your customizable low-code dashboard',
  backgroundColor = '#fef3c7', // light amber default
}) => {
  return (
    <section
      className="py-20 px-8 rounded-xl text-center"
      style={{ backgroundColor }}
    >
      <h1 className="text-4xl font-bold mb-4">{title}</h1>
      <p className="text-lg text-muted-foreground">{subtitle}</p>
    </section>
  )
}

export default HeroBanner
