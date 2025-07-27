// src/lib/mock/meta/menu.options.ts
import { MenuItem } from '@/types'

const menuOptions = {
  title: 'Admin Menu',
  type: 'menu',
  fields: [
    { label: 'Products', path: '/admin/products', icon: '📦' },
    { label: 'Inventory', path: '/admin/inventory', icon: '🏬' },
    { label: 'Orders', path: '/admin/orders', icon: '🧾' },
  ] as MenuItem[],
}

export default menuOptions
