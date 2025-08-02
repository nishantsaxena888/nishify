import HomeClientWrapper from '@/components/dynamic/home-client-wrapper'
import pagesConfig from '@/clients/pioneer_wholesale_inc/home.json'

export default function HomePage() {
  return <HomeClientWrapper sections={pagesConfig.sections} />
}
