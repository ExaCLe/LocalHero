import { Search, CheckCircle, Star } from "lucide-react";

export function HowItWorksSection() {
  const steps = [
    {
      icon: <Search className="h-7 w-7" />,
      title: "1. Entdecken",
      description: "Durchstöbere lokale Hilfsgesuche und finde ein Projekt, das zu deinen Fähigkeiten passt.",
    },
    {
      icon: <CheckCircle className="h-7 w-7" />,
      title: "2. Helfen",
      description: "Melde dich unkompliziert an und unterstütze das Projekt direkt vor Ort.",
    },
    {
      icon: <Star className="h-7 w-7" />,
      title: "3. Bestätigen",
      description: "Lass dir deinen Einsatz bestätigen, sammle Karma und erweitere dein Profil.",
    },
  ];

  return (
    <section className="relative overflow-hidden py-24 sm:py-32">
      {/* Background radial gradient */}
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-secondary/50 via-background to-background" />

      <div className="container mx-auto px-4">
        <div className="mb-20 text-center">
          <h2 className="text-3xl font-black tracking-tight sm:text-4xl md:text-5xl">
            So <span className="bg-gradient-to-r from-blue-500 to-primary bg-clip-text text-transparent">funktioniert&apos;s</span>
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-lg font-light text-muted-foreground">
            In drei einfachen Schritten vom Sofa direkt ins Ehrenamt.
          </p>
        </div>

        <div className="mx-auto max-w-5xl">
          <div className="relative flex flex-col justify-between gap-12 md:flex-row md:gap-8">
            {/* Connecting line for desktop with gradient */}
            <div className="absolute left-1/2 top-10 hidden h-0.5 w-[calc(100%-4rem)] -translate-x-1/2 -translate-y-1/2 bg-gradient-to-r from-transparent via-border to-transparent md:block" />

            {steps.map((step, index) => (
              <div key={index} className="group relative z-10 flex flex-1 flex-col items-center text-center">
                {/* Glow behind the icon on hover */}
                <div className="absolute top-0 h-20 w-20 scale-50 rounded-full bg-primary/30 opacity-0 blur-xl transition-all duration-500 group-hover:scale-150 group-hover:opacity-100" />
                
                <div className="relative mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-blue-600 text-white shadow-[0_0_40px_-10px_rgba(37,99,235,0.5)] ring-8 ring-background transition-transform duration-300 group-hover:-translate-y-2">
                  {step.icon}
                </div>
                
                <h3 className="mb-3 text-2xl font-bold tracking-tight">{step.title}</h3>
                <p className="max-w-[280px] leading-relaxed text-base text-muted-foreground">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
