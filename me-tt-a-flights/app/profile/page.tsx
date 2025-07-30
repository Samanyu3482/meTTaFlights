"use client"

import { useState, useEffect } from "react"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useAuth } from "@/components/auth-provider"
import { useToast } from "@/hooks/use-toast"
import { savedDetailsApiService, SavedPassenger, SavedPayment } from "@/lib/saved-details-api"
import { User, Mail, Phone, MapPin, Calendar, Award, Plane, Settings, Camera, Users, CreditCard, Plus, Edit, Trash2 } from "lucide-react"
import Link from "next/link"

export default function ProfilePage() {
  const { user, updateProfile } = useAuth()
  const { toast } = useToast()
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [profileData, setProfileData] = useState({
    name: "",
    email: "",
    phone: "",
    date_of_birth: "",
    nationality: "",
    address: "",
    emergency_contact: "",
  })
  const [savedPassengers, setSavedPassengers] = useState<SavedPassenger[]>([])
  const [savedPayments, setSavedPayments] = useState<SavedPayment[]>([])
  const [loadingSavedDetails, setLoadingSavedDetails] = useState(false)

  useEffect(() => {
    if (user) {
      setProfileData({
        name: user.name || "",
        email: user.email || "",
        phone: user.phone || "",
        date_of_birth: user.date_of_birth || "",
        nationality: user.nationality || "",
        address: user.address || "",
        emergency_contact: user.emergency_contact || "",
      })
    }
  }, [user])

  // Load saved passengers and payments
  useEffect(() => {
    const loadSavedDetails = async () => {
      if (user) {
        setLoadingSavedDetails(true)
        try {
          const [passengers, payments] = await Promise.all([
            savedDetailsApiService.getSavedPassengers(),
            savedDetailsApiService.getSavedPayments()
          ])
          setSavedPassengers(passengers)
          setSavedPayments(payments)
        } catch (error) {
          console.error('Error loading saved details:', error)
        } finally {
          setLoadingSavedDetails(false)
        }
      }
    }

    loadSavedDetails()
  }, [user])

  if (!user) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="container mx-auto px-4 py-20">
          <Card className="max-w-md mx-auto text-center">
            <CardContent className="p-8">
              <User className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
              <h2 className="text-2xl font-bold mb-4">Sign In Required</h2>
              <p className="text-muted-foreground mb-6">Please sign in to view your profile.</p>
              <Button asChild className="flight-gradient text-white">
                <Link href="/login">Sign In</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  const handleSave = async () => {
    setIsLoading(true)
    try {
      await updateProfile(profileData)
      toast({
        title: "Profile updated",
        description: "Your profile information has been saved successfully.",
      })
      setIsEditing(false)
    } catch (error) {
      toast({
        title: "Update failed",
        description: "Failed to update profile. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getMembershipColor = () => {
    // Simple membership tier based on account age
    const createdAt = new Date(user.created_at)
    const now = new Date()
    const monthsSinceCreation = (now.getTime() - createdAt.getTime()) / (1000 * 60 * 60 * 24 * 30)
    
    if (monthsSinceCreation > 24) return "bg-gray-800 text-white" // Platinum
    if (monthsSinceCreation > 12) return "bg-yellow-500 text-white" // Gold
    if (monthsSinceCreation > 6) return "bg-gray-400 text-white" // Silver
    return "bg-orange-500 text-white" // Bronze
  }

  const getMembershipTier = () => {
    const createdAt = new Date(user.created_at)
    const now = new Date()
    const monthsSinceCreation = (now.getTime() - createdAt.getTime()) / (1000 * 60 * 60 * 24 * 30)
    
    if (monthsSinceCreation > 24) return "Platinum"
    if (monthsSinceCreation > 12) return "Gold"
    if (monthsSinceCreation > 6) return "Silver"
    return "Bronze"
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        {/* Profile Header */}
        <div className="mb-8">
          <Card>
            <CardContent className="p-8">
              <div className="flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-6">
                <div className="relative">
                  <Avatar className="h-24 w-24">
                    <AvatarImage src="/placeholder-user.jpg" alt={user.name} />
                    <AvatarFallback className="text-2xl">
                      {user.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </AvatarFallback>
                  </Avatar>
                  <Button
                    size="icon"
                    variant="outline"
                    className="absolute -bottom-2 -right-2 h-8 w-8 rounded-full bg-transparent"
                  >
                    <Camera className="h-4 w-4" />
                  </Button>
                </div>

                <div className="text-center md:text-left flex-1">
                  <h1 className="text-3xl font-bold mb-2">{user.name}</h1>
                  <p className="text-muted-foreground mb-4">{user.email}</p>

                  <div className="flex flex-wrap items-center justify-center md:justify-start gap-4">
                    <Badge className={`${getMembershipColor()} px-3 py-1`}>
                      <Award className="h-4 w-4 mr-1" />
                      {getMembershipTier()} Member
                    </Badge>
                    <div className="flex items-center text-sm text-muted-foreground">
                      <Plane className="h-4 w-4 mr-1" />
                      Member since {new Date(user.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>

                <Button
                  onClick={() => setIsEditing(!isEditing)}
                  variant={isEditing ? "outline" : "default"}
                  className={!isEditing ? "flight-gradient text-white" : ""}
                  disabled={isLoading}
                >
                  <Settings className="h-4 w-4 mr-2" />
                  {isEditing ? "Cancel" : "Edit Profile"}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Profile Content */}
        <Tabs defaultValue="personal" className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="personal">Personal Info</TabsTrigger>
            <TabsTrigger value="saved">Saved Details</TabsTrigger>
            <TabsTrigger value="travel">Travel Preferences</TabsTrigger>
            <TabsTrigger value="loyalty">Loyalty Program</TabsTrigger>
            <TabsTrigger value="security">Security</TabsTrigger>
          </TabsList>

          <TabsContent value="personal" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Personal Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    value={profileData.name}
                    onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
                    disabled={!isEditing}
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="email"
                        value={profileData.email}
                        onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                        disabled={true} // Email cannot be changed
                        className="pl-10"
                      />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="phone">Phone Number</Label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="phone"
                        value={profileData.phone}
                        onChange={(e) => setProfileData({ ...profileData, phone: e.target.value })}
                        disabled={!isEditing}
                        className="pl-10"
                      />
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="dateOfBirth">Date of Birth</Label>
                    <div className="relative">
                      <Calendar className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input
                        id="dateOfBirth"
                        type="date"
                        value={profileData.date_of_birth}
                        onChange={(e) => setProfileData({ ...profileData, date_of_birth: e.target.value })}
                        disabled={!isEditing}
                        className="pl-10"
                      />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="nationality">Nationality</Label>
                    <Select
                      value={profileData.nationality}
                      onValueChange={(value) => setProfileData({ ...profileData, nationality: value })}
                      disabled={!isEditing}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="US">United States</SelectItem>
                        <SelectItem value="UK">United Kingdom</SelectItem>
                        <SelectItem value="CA">Canada</SelectItem>
                        <SelectItem value="AU">Australia</SelectItem>
                        <SelectItem value="IN">India</SelectItem>
                        <SelectItem value="DE">Germany</SelectItem>
                        <SelectItem value="FR">France</SelectItem>
                        <SelectItem value="JP">Japan</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div>
                  <Label htmlFor="address">Address</Label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="address"
                      value={profileData.address}
                      onChange={(e) => setProfileData({ ...profileData, address: e.target.value })}
                      disabled={!isEditing}
                      className="pl-10"
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="emergencyContact">Emergency Contact</Label>
                  <Input
                    id="emergencyContact"
                    value={profileData.emergency_contact}
                    onChange={(e) => setProfileData({ ...profileData, emergency_contact: e.target.value })}
                    disabled={!isEditing}
                    placeholder="Name - Phone Number"
                  />
                </div>

                {isEditing && (
                  <div className="flex space-x-4">
                    <Button 
                      onClick={handleSave} 
                      className="flight-gradient text-white"
                      disabled={isLoading}
                    >
                      {isLoading ? "Saving..." : "Save Changes"}
                    </Button>
                    <Button 
                      variant="outline" 
                      onClick={() => setIsEditing(false)}
                      disabled={isLoading}
                    >
                      Cancel
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="saved" className="mt-6">
            <div className="space-y-6">
              {/* Saved Passengers */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center">
                      <Users className="mr-2 h-5 w-5" />
                      Saved Passengers
                    </CardTitle>
                    <Button size="sm" variant="outline">
                      <Plus className="h-4 w-4 mr-2" />
                      Add Passenger
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  {loadingSavedDetails ? (
                    <div className="text-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
                      <p className="text-muted-foreground mt-2">Loading saved passengers...</p>
                    </div>
                  ) : savedPassengers.length === 0 ? (
                    <div className="text-center py-8">
                      <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <p className="text-muted-foreground mb-4">No saved passengers yet</p>
                      <p className="text-sm text-muted-foreground">Your passenger details will be saved automatically after your first booking.</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {savedPassengers.map((passenger) => (
                        <div key={passenger.id} className="flex items-center justify-between p-4 border rounded-lg">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2">
                              <h4 className="font-semibold">{passenger.first_name} {passenger.last_name}</h4>
                              {passenger.is_primary && (
                                <Badge variant="secondary" className="text-xs">Primary</Badge>
                              )}
                            </div>
                            <p className="text-sm text-muted-foreground">{passenger.email}</p>
                            <p className="text-sm text-muted-foreground">Passport: {passenger.passport_number}</p>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Button size="sm" variant="outline">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button size="sm" variant="outline" className="text-red-600 hover:text-red-700">
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Saved Payment Methods */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center">
                      <CreditCard className="mr-2 h-5 w-5" />
                      Saved Payment Methods
                    </CardTitle>
                    <Button size="sm" variant="outline">
                      <Plus className="h-4 w-4 mr-2" />
                      Add Payment Method
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  {loadingSavedDetails ? (
                    <div className="text-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
                      <p className="text-muted-foreground mt-2">Loading saved payments...</p>
                    </div>
                  ) : savedPayments.length === 0 ? (
                    <div className="text-center py-8">
                      <CreditCard className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <p className="text-muted-foreground mb-4">No saved payment methods yet</p>
                      <p className="text-sm text-muted-foreground">Your payment methods will be saved automatically after your first booking.</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {savedPayments.map((payment) => (
                        <div key={payment.id} className="flex items-center justify-between p-4 border rounded-lg">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2">
                              <h4 className="font-semibold">{payment.card_holder_name}</h4>
                              {payment.is_default && (
                                <Badge variant="secondary" className="text-xs">Default</Badge>
                              )}
                            </div>
                            <p className="text-sm text-muted-foreground">**** **** **** {payment.card_number}</p>
                            <p className="text-sm text-muted-foreground">Expires: {payment.expiry_month}/{payment.expiry_year}</p>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Button size="sm" variant="outline">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button size="sm" variant="outline" className="text-red-600 hover:text-red-700">
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* How to Use */}
              <Card>
                <CardHeader>
                  <CardTitle>How to Use Saved Details</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-start space-x-3">
                      <div className="w-6 h-6 bg-primary text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
                      <div>
                        <h4 className="font-semibold">Automatic Saving</h4>
                        <p className="text-sm text-muted-foreground">Your passenger and payment details are automatically saved after each successful booking.</p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-3">
                      <div className="w-6 h-6 bg-primary text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
                      <div>
                        <h4 className="font-semibold">Quick Booking</h4>
                        <p className="text-sm text-muted-foreground">When booking a flight, use the dropdown menus to quickly fill in saved passenger and payment details.</p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-3">
                      <div className="w-6 h-6 bg-primary text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
                      <div>
                        <h4 className="font-semibold">Manage Details</h4>
                        <p className="text-sm text-muted-foreground">Edit or remove saved details from this page anytime. Primary passengers and default payment methods are marked.</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="travel" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Travel Preferences</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label>Preferred Class</Label>
                    <Select defaultValue="economy">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="economy">Economy</SelectItem>
                        <SelectItem value="premium">Premium Economy</SelectItem>
                        <SelectItem value="business">Business</SelectItem>
                        <SelectItem value="first">First Class</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Seat Preference</Label>
                    <Select defaultValue="window">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="window">Window</SelectItem>
                        <SelectItem value="aisle">Aisle</SelectItem>
                        <SelectItem value="middle">Middle</SelectItem>
                        <SelectItem value="any">No Preference</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label>Meal Preference</Label>
                    <Select defaultValue="regular">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="regular">Regular</SelectItem>
                        <SelectItem value="vegetarian">Vegetarian</SelectItem>
                        <SelectItem value="vegan">Vegan</SelectItem>
                        <SelectItem value="kosher">Kosher</SelectItem>
                        <SelectItem value="halal">Halal</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Preferred Airlines</Label>
                    <Input placeholder="e.g., Delta, American, United" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="loyalty" className="mt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Loyalty Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center space-y-4">
                    <div className={`w-20 h-20 mx-auto ${getMembershipColor()} rounded-full flex items-center justify-center`}>
                      <Award className="h-10 w-10 text-white" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold">{getMembershipTier()} Member</h3>
                      <p className="text-muted-foreground">Since {new Date(user.created_at).toLocaleDateString()}</p>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Account Status</span>
                        <span className="font-bold text-green-600">Active</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Email Verified</span>
                        <span className={`font-bold ${user.is_verified ? 'text-green-600' : 'text-red-600'}`}>
                          {user.is_verified ? 'Yes' : 'No'}
                        </span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Benefits</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm">Priority booking</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm">Exclusive deals</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm">24/7 customer support</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                      <span className="text-sm text-muted-foreground">Lounge access (Platinum)</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                      <span className="text-sm text-muted-foreground">Upgrade priority (Platinum)</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="security" className="mt-6">
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Password & Security</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    Change Password
                  </Button>
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    Enable Two-Factor Authentication
                  </Button>
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    View Login History
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Privacy Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    Download My Data
                  </Button>
                  <Button variant="outline" className="w-full justify-start bg-transparent">
                    Privacy Preferences
                  </Button>
                  <Button variant="destructive" className="w-full justify-start">
                    Delete Account
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
