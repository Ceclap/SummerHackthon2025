import React, { useState, useRef, useEffect } from "react";
import {
  Upload,
  FileCheck2,
  Archive,
  BarChart2,
  FileText,
  Search,
  ChevronDown,
  LayoutGrid,
  Settings,
  HelpCircle,
} from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import GlassSphere from "@/components/ui/GlassSphere";
import Logo from "@/components/ui/Logo";

type Feature = {
  id: string;
  name: string;
  description: string;
  icon: React.ElementType;
  image: string;
};

const features: Feature[] = [
  {
    id: "upload",
    name: "Загрузка и Распознавание",
    description: "Мгновенно загружайте сканы или фото счетов-фактур и накладных.",
    icon: Upload,
    image: "/placeholder-1.jpg",
  },
  {
    id: "validation",
    name: "Валидация и Редактирование",
    description: "Автоматическая проверка данных и удобный интерфейс для исправлений.",
    icon: FileCheck2,
    image: "/placeholder-2.jpg",
  },
  {
    id: "archive",
    name: "Архив Документов",
    description: "Все документы в зашифрованном облаке с умным поиском.",
    icon: Archive,
    image: "/placeholder-3.jpg",
  },
  {
    id: "reports",
    name: "Отчеты и Аналитика",
    description: "Создавайте стандартные отчеты и анализируйте данные в один клик.",
    icon: BarChart2,
    image: "/placeholder-4.jpg",
  },
];

function App() {
  const [activeTab, setActiveTab] = useState("upload");
  const worksRef = useRef<HTMLDivElement>(null);

  const handleLearnMoreClick = () => {
    worksRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="min-h-screen w-full bg-background text-foreground relative aurora-bg">
      <Header onWorksClick={handleLearnMoreClick} />

      <main className="container mx-auto px-4 py-16 sm:py-24">
        <HeroSection onLearnMoreClick={handleLearnMoreClick} />
        <WorksSection ref={worksRef} features={features} />
      </main>

      <Footer />
    </div>
  );
}

const Header = ({ onWorksClick }: { onWorksClick: () => void }) => (
  <header className="fixed top-0 left-0 right-0 z-50">
    <nav className="container mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between glass-light rounded-b-xl">
      <Logo />
      <div className="hidden md:flex items-center gap-6">
        <a href="#works" onClick={(e) => { e.preventDefault(); onWorksClick(); }} className="text-sm font-medium hover:text-primary transition-colors">
          Возможности
        </a>
        <a href="#pricing" className="text-sm font-medium hover:text-primary transition-colors">
          Тарифы
        </a>
        <a href="#faq" className="text-sm font-medium hover:text-primary transition-colors">
          FAQ
        </a>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="ghost" className="text-sm">Войти</Button>
        <Button className="text-sm">Регистрация</Button>
      </div>
    </nav>
  </header>
);

const HeroSection = ({ onLearnMoreClick }: { onLearnMoreClick: () => void }) => (
  <section className="text-center flex flex-col items-center pt-20 pb-16">
    <GlassSphere />
    <h1 className="mt-12 text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight font-['Inter',system-ui,-apple-system,sans-serif] bg-gradient-to-r from-gray-900 via-blue-900 to-purple-900 bg-clip-text text-transparent">
      ContaSfera: Ваш умный помощник в бухгалтерии
    </h1>
    <p className="mt-4 max-w-2xl mx-auto text-lg text-muted-foreground font-['Inter',system-ui,-apple-system,sans-serif] font-medium">
      Загружайте, распознавайте и управляйте документами в несколько кликов.
      <br/>
      Автоматизация бухгалтерского учета для Молдовы.
    </p>
    <div className="mt-8 flex flex-wrap justify-center gap-4">
      <Button size="lg" onClick={onLearnMoreClick}>Начать работу</Button>
      <Button size="lg" variant="outline">Посмотреть демо</Button>
    </div>
  </section>
);

const WorksSection = React.forwardRef<HTMLDivElement, { features: Feature[] }>(({ features }, ref) => {
  const [selectedWork, setSelectedWork] = useState(features[0]);
  const [isIntersecting, setIntersecting] = useState(false);
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setIntersecting(entry.isIntersecting);
      },
      { rootMargin: "-100px" }
    );
    if (ref && typeof ref !== 'function' && ref.current) {
      observer.observe(ref.current);
    }
    return () => observer.disconnect();
  }, [ref]);

  return (
    <section id="works" ref={ref} className="py-16 sm:py-24">
      <div className="text-left mb-12">
        <h2 className="text-4xl font-bold tracking-tight font-['Inter',system-ui,-apple-system,sans-serif] bg-gradient-to-r from-gray-900 via-blue-900 to-purple-900 bg-clip-text text-transparent">Возможности</h2>
        <p className="mt-2 text-lg text-muted-foreground font-['Inter',system-ui,-apple-system,sans-serif] font-medium">
          От сканирования документов до готовых отчетов — откройте для себя все функции ContaSfera.
        </p>
      </div>
      <div className="grid md:grid-cols-2 gap-8 lg:gap-12 items-start">
        <div className="flex flex-col gap-4">
          {features.map((work) => (
            <Card
              key={work.id}
              onClick={() => setSelectedWork(work)}
              className={cn(
                "cursor-pointer transition-all duration-300 hover-lift",
                selectedWork.id === work.id ? "bg-white/80 shadow-lg" : "glass-light"
              )}
            >
              <CardHeader className="flex flex-row items-center gap-4">
                <div className="p-3 bg-primary/10 rounded-lg">
                  <work.icon className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <CardTitle className="font-['Inter',system-ui,-apple-system,sans-serif] font-semibold">{work.name}</CardTitle>
                  <CardDescription className="font-['Inter',system-ui,-apple-system,sans-serif] font-medium">{work.description}</CardDescription>
                </div>
              </CardHeader>
            </Card>
          ))}
        </div>
        <div className="relative h-96 md:h-full rounded-xl overflow-hidden glass-light hover-lift">
          <img src={selectedWork.image} alt={selectedWork.name} className="object-cover w-full h-full" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
          <div className="absolute bottom-4 left-4 text-white">
            <h3 className="font-bold text-xl font-['Inter',system-ui,-apple-system,sans-serif]">{selectedWork.name}</h3>
          </div>
        </div>
      </div>
    </section>
  );
});

const Footer = () => (
  <footer className="border-t">
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col sm:flex-row justify-between items-center">
      <p className="text-sm text-muted-foreground">&copy; {new Date().getFullYear()} ContaSfera. Все права защищены.</p>
      <div className="flex gap-4 mt-4 sm:mt-0">
        <a href="#" className="text-muted-foreground hover:text-primary"><Settings className="w-5 h-5"/></a>
        <a href="#" className="text-muted-foreground hover:text-primary"><HelpCircle className="w-5 h-5"/></a>
      </div>
    </div>
  </footer>
);

export default App;
