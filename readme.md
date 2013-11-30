# Highway
Highway is a simple app for updating Route53 with wildcard domains.

* `docker build -t highway .`
* `docker run -p 8000 highway`

# Environment

* `AWS_ACCESS_KEY_ID`: AWS Access ID
* `AWS_SECRET_ACCESS_KEY`: AWS Secret Key
* `BASE_DOMAIN`: Base record to use for adding (i.e. `foo.mydomain.com`)
* `R53_ZONE`: Route53 Zone
* `GOOGLE_ANALYTICS_CODE`: (optional) Google Analytics
* `RECORD_TTL`: Record time-to-live in seconds (default: 3600)
* `SOCIAL_AUTH_GITHUB_KEY`: Github auth key
* `SOCIAL_AUTH_GITHUB_SECRET`: Github auth secret
* `SOCIAL_AUTH_TWITTER_KEY`: Twitter auth key
* `SOCIAL_AUTH_TWITTER_SECRET`: Twitter auth secret

Various icons from the Iconic (http://somerandomdude.com/work/iconic/) project.
