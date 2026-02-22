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
    <section className="relative overflow-hidden bg-gradient-to-b from-secondary/40 via-background to-background py-24 sm:py-32">
      {/* Decorative background blobs */}
      <div className="absolute left-0 top-1/4 -z-10 h-72 w-72 -translate-x-1/2 rounded-full bg-primary/5 blur-[100px]" />
      <div className="absolute right-0 bottom-1/4 -z-10 h-96 w-96 translate-x-1/3 rounded-full bg-blue-500/5 blur-[100px]" />

      <div className="container mx-auto px-4">
        <div className="mb-20 text-center">
          <h2 className="text-3xl font-black tracking-tight sm:text-4xl md:text-5xl">
            Warum <span className="text-primary text-transparent bg-clip-text bg-gradient-to-r from-primary to-blue-500">LocalHero</span>?
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-lg font-light text-muted-foreground">
            Die moderne Art, sich zu engagieren. Ohne starre Vereinsstrukturen,
            aber mit maximalem Impact.
          </p>
        </div>

        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group relative overflow-hidden rounded-2xl border border-white/20 bg-background/60 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-2 hover:shadow-xl hover:shadow-primary/10 dark:border-white/10"
            >
              {/* Inner subtle gradient on hover */}
              <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
              
              <div className="relative z-10">
                <div className="mb-6 inline-flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 shadow-inner ring-1 ring-primary/20">
                  <div className="transition-transform duration-300 group-hover:scale-110">
                    {feature.icon}
                  </div>
                </div>
                <h3 className="mb-3 text-xl font-bold tracking-tight">{feature.title}</h3>
                <p className="leading-relaxed text-muted-foreground">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
