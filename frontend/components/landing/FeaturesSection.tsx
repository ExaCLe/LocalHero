import { Heart, Calendar, Award, Users } from "lucide-react";

export function FeaturesSection() {
  const features = [
    {
      icon: <Heart className="h-8 w-8 text-primary" />,
      title: "Ehrenamt trifft Dating",
      description:
        "Finde Projekte, die wirklich zu dir passen. Matche mit Vereinen unkompliziert wie auf einer Dating-Plattform.",
    },
    {
      icon: <Calendar className="h-8 w-8 text-primary" />,
      title: "Flexibel Helfen",
      description:
        "Keine langfristigen Verpflichtungen. Bestätige deine Hilfe einmalig für Tag X und Uhrzeit Y.",
    },
    {
      icon: <Award className="h-8 w-8 text-primary" />,
      title: "Gamification & Historie",
      description:
        "Lass dir deine Hilfe bestätigen und baue deine Historie auf. Sammle Karma-Punkte für deine gute Taten.",
    },
    {
      icon: <Users className="h-8 w-8 text-primary" />,
      title: "Community Connect",
      description:
        "Lerne neue Leute kennen und vernetze dich mit Gleichgesinnten, während ihr gemeinsam die Welt verbessert.",
    },
  ];

  return (
    <section className="bg-secondary/50 py-24">
      <div className="container mx-auto px-4">
        <div className="mb-16 text-center">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Warum LocalHero?
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Die moderne Art, sich zu engagieren.
          </p>
        </div>

        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group relative overflow-hidden rounded-lg border bg-background p-6 shadow-sm transition-shadow hover:shadow-md"
            >
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                {feature.icon}
              </div>
              <h3 className="mb-2 text-xl font-bold">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
