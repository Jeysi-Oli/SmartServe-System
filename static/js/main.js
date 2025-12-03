document.addEventListener("DOMContentLoaded", () => {
  // Contact Form Handler
  const contactForm = document.getElementById("contactForm")
  if (contactForm) {
    contactForm.addEventListener("submit", async (e) => {
      e.preventDefault()

      const formData = new FormData(contactForm)
      const data = Object.fromEntries(formData)

      try {
        const response = await fetch("/api/contact", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        })

        const result = await response.json()

        if (result.success) {
          alert("Thank you! Your message has been sent successfully.")
          contactForm.reset()
        } else {
          alert("An error occurred. Please try again.")
        }
      } catch (error) {
        console.error("Error:", error)
        alert("An error occurred. Please try again.")
      }
    })
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({ behavior: "smooth" })
      }
    })
  })

  // Active navigation link
  const navLinks = document.querySelectorAll(".nav-links a")
  const currentPage = window.location.pathname

  navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentPage) {
      link.style.color = "var(--primary-color)"
      link.style.borderBottom = "2px solid var(--primary-color)"
    }
  })
})
