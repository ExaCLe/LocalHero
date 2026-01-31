import { Search, CheckCircle, Star } from "lucide-react";

export function HowItWorksSection() {
  const steps = [
    {
      icon: <Search className="h-6 w-6" />,
      title: "Entdecken",
      description: "Durchstöbere lokale Hilfsgesuche und finde ein Projekt.",
    },
    {
      icon: <CheckCircle className="h-6 w-6" />,
      title: "Helfen",
      description: "Melde dich an und unterstütze das Projekt vor Ort.",
    },
    {
      icon: <Star className="h-6 w-6" />,
      title: "Bestätigen",
      description: "Lass dir deinen Einsatz bestätigen und erweitere dein Profil.",
    },
  ];

  return (
    <section className="py-24">
      <div className="container mx-auto px-4">
        <div className="mb-16 text-center">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            So funktioniert&apos;s
          </h2>
        </div>

        <div className="mx-auto max-w-4xl">
          <div className="relative flex flex-col justify-between gap-8 md:flex-row">
            {/* Connecting line for desktop */}
            <div className="absolute top-8 left-0 hidden h-0.5 w-full -translate-y-1/2 bg-border md:block" />

            {steps.map((step, index) => (
              <div key={index} className="relative z-10 flex flex-col items-center text-center">
                <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg ring-4 ring-background">
                  {step.icon}
                </div>
                <h3 className="mb-2 text-lg font-bold">{step.title}</h3>
                <p className="max-w-[250px] text-sm text-muted-foreground">
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
