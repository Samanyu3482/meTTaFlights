import { Navigation } from "@/components/navigation"
import { HomeSearch } from "@/components/home-search"
import { TypewriterText } from "@/components/typewriter-text"
import { AnimatedCounter } from "@/components/animated-counter"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Star, MapPin, Clock, Shield, Award, Plane, Globe } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

const featuredDestinations = [
  {
    city: "Paris",
    country: "France",
    price: "from $599",
    image: "/destinations/paris.jpg",
    description: "City of Light and Romance",
  },
  {
    city: "Tokyo",
    country: "Japan",
    price: "from $899",
    image: "/destinations/tokyo.jpg",
    description: "Modern metropolis meets tradition",
  },
  {
    city: "New York",
    country: "USA",
    price: "from $399",
    image: "/destinations/newyork.jpg",
    description: "The city that never sleeps",
  },
  {
    city: "London",
    country: "UK",
    price: "from $549",
    image: "/destinations/london.jpg",
    description: "Historic charm and modern culture",
  },
  {
    city: "Rome",
    country: "Italy",
    price: "from $699",
    image: "/destinations/rome.jpg",
    description: "Eternal city of history and culture",
  },
  {
    city: "Barcelona",
    country: "Spain",
    price: "from $649",
    image: "/destinations/barcelona.jpg",
    description: "Mediterranean charm and architecture",
  },
  {
    city: "Dubai",
    country: "UAE",
    price: "from $799",
    image: "/destinations/dubai.jpg",
    description: "Luxury and futuristic architecture",
  },
  {
    city: "Singapore",
    country: "Singapore",
    price: "from $749",
    image: "/destinations/singapore.jpg",
    description: "Garden city of innovation",
  },
]

const testimonials = [
  {
    name: "Sarah Johnson",
    rating: 5,
    comment: "Amazing service! Found the perfect flight at an unbeatable price. The booking process was seamless.",
    avatar: "/testimonials/sarah.jpg",
  },
  {
    name: "Michael Chen",
    rating: 5,
    comment: "Best flight booking experience ever. Great customer support and easy cancellation policy.",
    avatar: "/testimonials/michael.jpg",
  },
  {
    name: "Emma Davis",
    rating: 5,
    comment: "Love the user interface and how easy it is to compare different airlines. Highly recommended!",
    avatar: "/testimonials/emma.jpg",
  },
  {
    name: "David Rodriguez",
    rating: 5,
    comment: "Incredible deals and the search filters are so helpful. Found exactly what I was looking for!",
    avatar: "/testimonials/david.jpg",
  },
  {
    name: "Lisa Thompson",
    rating: 5,
    comment: "The mobile app is fantastic! Booked my entire trip in minutes. Customer service is top-notch.",
    avatar: "/testimonials/lisa.jpg",
  },
]

const features = [
  {
    icon: Shield,
    title: "Secure Booking",
    description: "Your data is protected with bank-level security",
  },
  {
    icon: Award,
    title: "Best Prices",
    description: "We guarantee the lowest prices or we'll match them",
  },
  {
    icon: Clock,
    title: "24/7 Support",
    description: "Round-the-clock customer service for your peace of mind",
  },
  {
    icon: Globe,
    title: "Global Coverage",
    description: "Access to flights from 500+ airlines worldwide",
  },
]

const typewriterTexts = [
  "Find Your Perfect Flight",
  "Book With Confidence",
  "Travel The World",
  "Discover Amazing Deals",
  "Your Journey Starts Here",
]

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-purple-50 via-white to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        <div className="container mx-auto px-4 py-20">
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center p-2 bg-primary/10 rounded-full mb-6">
              <Plane className="h-8 w-8 text-primary animate-float" />
            </div>

            {/* Typewriter Animation */}
            <div className="h-20 flex items-center justify-center mb-6">
              <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                <TypewriterText texts={typewriterTexts} speed={100} deleteSpeed={50} pauseTime={2000} />
              </h1>
            </div>

            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto animate-slide-up">
              Discover amazing destinations, compare prices from hundreds of airlines, and book your perfect flight with
              confidence.
            </p>

            {/* Animated Statistics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12 max-w-4xl mx-auto">
              <Card className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105">
                <CardContent className="p-4">
                  <div className="text-2xl md:text-3xl font-bold text-primary mb-1">
                    <AnimatedCounter end={50000} suffix="+" />
                  </div>
                  <p className="text-sm text-muted-foreground">Happy Customers</p>
                </CardContent>
              </Card>

              <Card className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105">
                <CardContent className="p-4">
                  <div className="text-2xl md:text-3xl font-bold text-primary mb-1">
                    <AnimatedCounter end={125000} suffix="+" />
                  </div>
                  <p className="text-sm text-muted-foreground">Flights Booked</p>
                </CardContent>
              </Card>

              <Card className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105">
                <CardContent className="p-4">
                  <div className="text-2xl md:text-3xl font-bold text-primary mb-1">
                    <AnimatedCounter end={500} suffix="+" />
                  </div>
                  <p className="text-sm text-muted-foreground">Destinations</p>
                </CardContent>
              </Card>

              <Card className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105">
                <CardContent className="p-4">
                  <div className="text-2xl md:text-3xl font-bold text-primary mb-1">
                    <AnimatedCounter end={50} suffix="+" />
                  </div>
                  <p className="text-sm text-muted-foreground">Countries</p>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Search Widget */}
          <div className="max-w-4xl mx-auto">
            <HomeSearch />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-muted/50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Why Choose meTTaFlights?</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              We make flight booking simple, secure, and affordable for everyone.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-all duration-300 hover:scale-105">
                <CardHeader>
                  <div className="mx-auto w-12 h-12 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center mb-4">
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Destinations */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Popular Destinations</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Explore the world's most amazing destinations with unbeatable flight deals.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredDestinations.map((destination, index) => (
              <Card
                key={index}
                className="overflow-hidden hover:shadow-lg transition-all duration-300 group cursor-pointer hover:scale-105"
              >
                <div className="relative h-48 overflow-hidden">
                  <Image
                    src={destination.image || "/placeholder.svg"}
                    alt={destination.city}
                    fill
                    className="object-cover group-hover:scale-110 transition-transform duration-300"
                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                  />
                  <div className="absolute top-4 right-4">
                    <Badge className="bg-white/90 text-black">{destination.price}</Badge>
                  </div>
                </div>
                <CardContent className="p-4">
                  <div className="flex items-center mb-2">
                    <MapPin className="h-4 w-4 text-muted-foreground mr-1" />
                    <span className="text-sm text-muted-foreground">{destination.country}</span>
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{destination.city}</h3>
                  <p className="text-muted-foreground text-sm">{destination.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center mt-12">
            <Button asChild size="lg" className="flight-gradient text-white hover:scale-105 transition-transform">
              <Link href="/destinations">Explore All Destinations</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 bg-muted/50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">What Our Travelers Say</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Join millions of satisfied customers who trust us with their travel plans.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="hover:shadow-lg transition-all duration-300 hover:scale-105">
                <CardContent className="p-6">
                  <div className="flex items-center mb-4">
                    <Image
                      src={testimonial.avatar || "/placeholder.svg"}
                      alt={testimonial.name}
                      width={48}
                      height={48}
                      className="rounded-full mr-4 object-cover"
                    />
                    <div>
                      <h4 className="font-semibold">{testimonial.name}</h4>
                      <div className="flex">
                        {[...Array(testimonial.rating)].map((_, i) => (
                          <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        ))}
                      </div>
                    </div>
                  </div>
                  <p className="text-muted-foreground italic">"{testimonial.comment}"</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 flight-gradient text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Start Your Journey?</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Join millions of travelers who trust meTTaFlights for their adventures around the world.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="secondary" asChild className="hover:scale-105 transition-transform">
              <Link href="/register">Sign Up Free</Link>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="bg-transparent border-white text-white hover:bg-white hover:text-purple-600 hover:scale-105 transition-all"
              asChild
            >
              <Link href="/flights">Search Flights</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-background border-t py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-full flight-gradient">
                  <Plane className="h-4 w-4 text-white" />
                </div>
                <span className="text-xl font-bold">meTTaFlights</span>
              </div>
              <p className="text-muted-foreground">
                Your trusted partner for flight bookings worldwide. Making travel accessible and affordable for
                everyone.
              </p>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li>
                  <Link href="/about" className="hover:text-primary transition-colors">
                    About Us
                  </Link>
                </li>
                <li>
                  <Link href="/careers" className="hover:text-primary transition-colors">
                    Careers
                  </Link>
                </li>
                <li>
                  <Link href="/press" className="hover:text-primary transition-colors">
                    Press
                  </Link>
                </li>
                <li>
                  <Link href="/blog" className="hover:text-primary transition-colors">
                    Blog
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li>
                  <Link href="/help" className="hover:text-primary transition-colors">
                    Help Center
                  </Link>
                </li>
                <li>
                  <Link href="/contact" className="hover:text-primary transition-colors">
                    Contact Us
                  </Link>
                </li>
                <li>
                  <Link href="/terms" className="hover:text-primary transition-colors">
                    Terms of Service
                  </Link>
                </li>
                <li>
                  <Link href="/privacy" className="hover:text-primary transition-colors">
                    Privacy Policy
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Travel</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li>
                  <Link href="/destinations" className="hover:text-primary transition-colors">
                    Destinations
                  </Link>
                </li>
                <li>
                  <Link href="/deals" className="hover:text-primary transition-colors">
                    Flight Deals
                  </Link>
                </li>
                <li>
                  <Link href="/airlines" className="hover:text-primary transition-colors">
                    Airlines
                  </Link>
                </li>
                <li>
                  <Link href="/travel-guide" className="hover:text-primary transition-colors">
                    Travel Guide
                  </Link>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t mt-8 pt-8 text-center text-muted-foreground">
            <p>&copy; 2024 meTTaFlights. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
