import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AnimatedCounter } from "@/components/animated-counter"
import { Plane, Heart, Target, Eye, Zap, Database, Cpu, Globe, Users, GraduationCap, User, BookOpen, Code } from "lucide-react"
import Link from "next/link"

const teamMembers = [
  {
    name: "Samanyu Gautam",
    role: "Lead Developer & AI Engineer",
    icon: User,
    bio: "CSE-AI Student at Chitkara University, specializing in MeTTa and AI technologies",
  },
  {
    name: "Dr. Sushil Narang",
    role: "Dean & Project Guide",
    icon: User,
    bio: "Dean of Engineering at Chitkara University, providing academic guidance",
  },
  {
    name: "Dr. Vandana Mohindru Sood",
    role: "Faculty Mentor",
    icon: User,
    bio: "Faculty mentor providing technical and academic support for the project",
  },
  {
    name: "Krubl Sir",
    role: "Technical Advisor",
    icon: User,
    bio: "Singularity Net MeTTa expert, guiding MeTTa integration and knowledge representation",
  },
]

const values = [
  {
    icon: Heart,
    title: "Innovation First",
    description: "Pioneering AI and MeTTa technology in travel industry",
  },
  {
    icon: Target,
    title: "Academic Excellence",
    description: "Demonstrating practical application of advanced AI concepts",
  },
  {
    icon: Eye,
    title: "User-Centric Design",
    description: "Creating intuitive and accessible flight booking experiences",
  },
  {
    icon: Zap,
    title: "Performance",
    description: "Lightning-fast search across 75K+ flights with AI optimization",
  },
]

const techStats = [
  {
    icon: Database,
    title: "Flight Records",
    value: 75654,
    suffix: "+",
    description: "Comprehensive flight database"
  },
  {
    icon: Globe,
    title: "Airports",
    value: 103,
    description: "US domestic airports covered"
  },
  {
    icon: Cpu,
    title: "API Response",
    value: 500,
    suffix: "ms",
    description: "Average search time"
  },
  {
    icon: Users,
    title: "Concurrent Users",
    value: 1000,
    suffix: "+",
    description: "System capacity"
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
              About MeTTa-Flights
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              An AI-powered flight booking system developed by Samanyu Gautam (CSE-AI, Chitkara University) 
              under the guidance of Dr. Sushil Narang, Dr. Vandana Mohindru Sood, and Krubl Sir from Singularity Net MeTTa.
            </p>
            <div className="mt-6">
              <Badge variant="secondary" className="text-sm">
                Academic Project 2024-2025
              </Badge>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {techStats.map((stat, index) => (
              <Card key={index} className="text-center">
                <CardContent className="p-6">
                  <div className="flex justify-center mb-3">
                    <stat.icon className="h-8 w-8 text-primary" />
                  </div>
                  <div className="text-3xl font-bold text-primary mb-2">
                    <AnimatedCounter end={stat.value} suffix={stat.suffix || ""} />
                  </div>
                  <p className="text-sm font-medium mb-1">{stat.title}</p>
                  <p className="text-xs text-muted-foreground">{stat.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Our Story */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">Project Story</h2>
              <div className="space-y-4 text-muted-foreground">
                <p>
                  MeTTa-Flights is an innovative academic project that demonstrates the practical application of 
                  cutting-edge AI technologies in the travel industry. Developed as part of the Computer Science 
                  Engineering - Artificial Intelligence program at Chitkara University, Punjab, India.
                </p>
                <p>
                  The project showcases the integration of MeTTa (Meta Type Theory) knowledge representation system 
                  with modern web technologies to create a comprehensive flight booking platform. With 75,654 flight 
                  records and 103 airports, it represents one of the largest academic implementations of MeTTa technology.
                </p>
                <p>
                  Under the guidance of Dr. Sushil Narang (Dean), Dr. Vandana Mohindru Sood (Faculty Mentor), and 
                  Krubl Sir from Singularity Net MeTTa, this project demonstrates how academic learning can be 
                  translated into practical, real-world applications that benefit society.
                </p>
              </div>
            </div>
            <div className="relative">
              <img 
                src="/chitkara/chitkara-university-logo.png" 
                alt="Chitkara University Logo" 
                className="rounded-lg shadow-lg w-full h-auto max-w-md mx-auto"
              />
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
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Project Contributors</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              The dedicated team behind MeTTa-Flights, combining academic excellence with technical innovation.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {teamMembers.map((member, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105">
                <CardContent className="p-6">
                  <div className="mx-auto w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                    <member.icon className="h-12 w-12 text-primary" />
                  </div>
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

      {/* Special Thanks to Parents */}
      <section className="py-20 bg-gradient-to-r from-pink-50 to-purple-50 dark:from-gray-900 dark:to-gray-800">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center justify-center p-3 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full mb-6">
              <Heart className="h-8 w-8 text-white" />
            </div>
            <h2 className="text-3xl md:text-4xl font-bold mb-4 bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
              Special Thanks to My Parents
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              This project would not have been possible without the unwavering support, love, and guidance of my parents.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <Card className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105 border-2 border-pink-200 dark:border-pink-800">
              <CardContent className="p-8">
                <div className="mx-auto w-24 h-24 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center mb-6">
                  <GraduationCap className="h-12 w-12 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-2 text-blue-600 dark:text-blue-400">Dr. Vishal Gautam</h3>
                <Badge variant="outline" className="mb-4 bg-blue-50 dark:bg-blue-900/20">
                  My Father
                </Badge>
                <p className="text-muted-foreground">
                  Thank you for your constant encouragement, wisdom, and for believing in my dreams. 
                  Your guidance has been the foundation of my academic journey.
                </p>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105 border-2 border-purple-200 dark:border-purple-800">
              <CardContent className="p-8">
                <div className="mx-auto w-24 h-24 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center mb-6">
                  <BookOpen className="h-12 w-12 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-2 text-purple-600 dark:text-purple-400">Dr. Bindu Sharma</h3>
                <Badge variant="outline" className="mb-4 bg-purple-50 dark:bg-purple-900/20">
                  My Mother
                </Badge>
                <p className="text-muted-foreground">
                  Thank you for your endless love, patience, and for being my biggest supporter. 
                  Your strength and dedication inspire me every day.
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="text-center mt-12">
            <p className="text-lg text-muted-foreground italic">
              "Behind every successful student, there are parents who believed in them when no one else did."
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 flight-gradient text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Experience the Future of Flight Booking</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Discover how AI and MeTTa technology are revolutionizing the travel industry through this innovative academic project.
          </p>
          <Button size="lg" variant="secondary" asChild className="hover:scale-105 transition-transform">
            <Link href="/flights">Start Exploring</Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
