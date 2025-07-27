import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AnimatedCounter } from "@/components/animated-counter"
import { Plane, Heart, Target, Eye, Zap } from "lucide-react"
import Link from "next/link"

const teamMembers = [
  {
    name: "Sarah Johnson",
    role: "CEO & Founder",
    image: "/placeholder.svg?height=200&width=200",
    bio: "Former airline executive with 15+ years in aviation industry",
  },
  {
    name: "Michael Chen",
    role: "CTO",
    image: "/placeholder.svg?height=200&width=200",
    bio: "Tech visionary specializing in travel technology and AI",
  },
  {
    name: "Emma Davis",
    role: "Head of Operations",
    image: "/placeholder.svg?height=200&width=200",
    bio: "Operations expert ensuring seamless customer experiences",
  },
  {
    name: "David Wilson",
    role: "Head of Customer Success",
    image: "/placeholder.svg?height=200&width=200",
    bio: "Customer advocate with passion for exceptional service",
  },
]

const values = [
  {
    icon: Heart,
    title: "Customer First",
    description: "Every decision we make puts our customers at the center",
  },
  {
    icon: Target,
    title: "Innovation",
    description: "Constantly improving and innovating to serve you better",
  },
  {
    icon: Eye,
    title: "Transparency",
    description: "Clear pricing, honest communication, no hidden fees",
  },
  {
    icon: Zap,
    title: "Efficiency",
    description: "Making flight booking fast, simple, and hassle-free",
  },
]

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-br from-purple-50 via-white to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center justify-center p-3 bg-primary/10 rounded-full mb-6">
              <Plane className="h-8 w-8 text-primary" />
            </div>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              About meTTaFlights
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              We're on a mission to make travel accessible, affordable, and amazing for everyone. Since 2020, we've been
              connecting travelers with their dream destinations.
            </p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            <Card className="text-center">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-primary mb-2">
                  <AnimatedCounter end={4} />
                </div>
                <p className="text-muted-foreground">Years of Excellence</p>
              </CardContent>
            </Card>
            <Card className="text-center">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-primary mb-2">
                  <AnimatedCounter end={2000000} suffix="+" />
                </div>
                <p className="text-muted-foreground">Happy Travelers</p>
              </CardContent>
            </Card>
            <Card className="text-center">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-primary mb-2">
                  <AnimatedCounter end={500} suffix="+" />
                </div>
                <p className="text-muted-foreground">Partner Airlines</p>
              </CardContent>
            </Card>
            <Card className="text-center">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-primary mb-2">
                  <AnimatedCounter end={195} />
                </div>
                <p className="text-muted-foreground">Countries Served</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Our Story */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">Our Story</h2>
              <div className="space-y-4 text-muted-foreground">
                <p>
                  meTTaFlights was born from a simple frustration: booking flights was too complicated, expensive, and
                  time-consuming. Our founders, experienced travelers themselves, knew there had to be a better way.
                </p>
                <p>
                  In 2020, we set out to revolutionize flight booking by creating a platform that combines cutting-edge
                  technology with genuine care for our customers. We believe that everyone deserves access to affordable
                  travel options without the hassle.
                </p>
                <p>
                  Today, we're proud to serve millions of travelers worldwide, helping them discover new destinations
                  and create unforgettable memories. Our journey is just beginning, and we're excited to have you along
                  for the ride.
                </p>
              </div>
            </div>
            <div className="relative">
              <img src="/placeholder.svg?height=400&width=600" alt="Our Story" className="rounded-lg shadow-lg" />
            </div>
          </div>
        </div>
      </section>

      {/* Our Values */}
      <section className="py-20 bg-muted/50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Values</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              These core values guide everything we do and shape how we serve our customers.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105">
                <CardHeader>
                  <div className="mx-auto w-12 h-12 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center mb-4">
                    <value.icon className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-xl">{value.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{value.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Meet Our Team</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              The passionate people behind meTTaFlights, working hard to make your travel dreams come true.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {teamMembers.map((member, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105">
                <CardContent className="p-6">
                  <img
                    src={member.image || "/placeholder.svg"}
                    alt={member.name}
                    className="w-24 h-24 rounded-full mx-auto mb-4 object-cover"
                  />
                  <h3 className="text-xl font-semibold mb-2">{member.name}</h3>
                  <Badge variant="secondary" className="mb-3">
                    {member.role}
                  </Badge>
                  <p className="text-sm text-muted-foreground">{member.bio}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 flight-gradient text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Join Our Journey?</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Experience the meTTaFlights difference and discover why millions of travelers trust us.
          </p>
          <Button size="lg" variant="secondary" asChild className="hover:scale-105 transition-transform">
            <Link href="/register">Start Your Adventure</Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
