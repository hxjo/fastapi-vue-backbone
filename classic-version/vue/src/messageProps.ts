export interface MessageProps {
  message?: {
    content: string
    timestamp: number
    type: 'error' | 'default'
  }
}
