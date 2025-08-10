'use client'

import React from 'react'
import { getDynamicComponent } from './dynamic-loader'

type SectionConfig = {
  type: string
  [key: string]: any
}

type Props = {
  sections: SectionConfig[]
}

const HomeClientWrapper: React.FC<Props> = ({ sections }) => {
  return (
    <div className="space-y-8 p-6">
      ssnnn
      {sections.map((section, index) => {
        const Component = getDynamicComponent(section.type)
        if (!Component) {
          return (
            <div key={index} className="text-red-500">
              ⚠ Missing component: <strong>{section.type}</strong>
            </div>
          )
        }
        return <Component key={index} {...section} />
      })}
    </div>
  )
}

export default HomeClientWrapper
