export interface DocumentData {
  id: number;
  type: string;
  number: string;
  date: string;
  seller: string;
  buyer: string;
  idno: string;
  amount: string;
  vat: string;
  total: string;
  status: 'pending' | 'validated' | 'archived';
  errors?: number;
}

export interface UploadProgress {
  isUploading: boolean;
  progress: number;
  extractedData: DocumentData | null;
}

export interface ValidationDocument {
  id: number;
  type: string;
  number: string;
  date: string;
  status: 'pending' | 'validated';
  errors: number;
  amount: string;
}

export interface ArchiveDocument {
  id: number;
  type: string;
  number: string;
  date: string;
  status: 'archived';
  amount: string;
}

export interface Statistics {
  total: number;
  withErrors: number;
  withoutErrors: number;
  totalAmount: string;
} 