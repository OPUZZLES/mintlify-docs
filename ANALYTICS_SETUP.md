# Analytics Setup Guide

## Google Analytics 4 Configuration

1. **Create GA4 Property**:
   - Go to [Google Analytics](https://analytics.google.com)
   - Create a new GA4 property for `blog.educate-ai.com`
   - Copy your Measurement ID (format: `G-XXXXXXXXXX`)

2. **Update mint.json**:
   ```json
   "analytics": {
     "gtag": {
       "measurementId": "G-XXXXXXXXXX"  // Replace with your actual ID
     }
   }
   ```

## Plausible Analytics (Alternative)

Plausible is already configured in `mint.json` for `blog.educate-ai.com`. To activate:

1. **Sign up for Plausible**:
   - Go to [Plausible.io](https://plausible.io)
   - Add your domain: `blog.educate-ai.com`

2. **No code changes needed** - configuration is already in place!

## What You'll Track

### Automatic Tracking
- **Page views** and unique visitors
- **Traffic sources** (Google, social media, direct)
- **Popular content** and reading patterns
- **Device/browser** information
- **Geographic** data

### Custom Events (Optional)
You can add custom tracking for:
- Newsletter signups
- Social media shares
- Download clicks
- Time spent reading

### Key Metrics to Monitor
- **Most popular posts** and categories
- **Bounce rate** and session duration
- **Conversion rate** for newsletter signups
- **Traffic growth** over time
- **Referral sources** and SEO performance

## Privacy Compliance

Both analytics solutions are configured to be privacy-friendly:
- **No cookies** required (Plausible)
- **GDPR compliant** out of the box
- **Anonymized** visitor data
- **Lightweight** impact on page load

## Dashboard Access

Once configured, you can access your analytics:
- **Google Analytics**: analytics.google.com
- **Plausible**: plausible.io/blog.educate-ai.com

## Additional Tracking (Optional)

### Search Console
Set up Google Search Console for SEO insights:
1. Add `blog.educate-ai.com` to Search Console
2. Submit your sitemap: `https://blog.educate-ai.com/sitemap.xml`

### Social Media Analytics
Track social media performance:
- LinkedIn Analytics for company page
- Twitter Analytics if you create an account
- Newsletter platform analytics (Mailchimp, ConvertKit, etc.)

---

*Remember to update the Measurement ID in `mint.json` with your actual Google Analytics ID!*