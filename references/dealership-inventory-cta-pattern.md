# Dealership Inventory CTA Pattern

Purpose: keep model CTA links consistent across dealership content pages and comparison pages.

## Rule
For model-specific shopping CTAs, use the dealership's live filtered inventory URL when available.

Do **not** default to generic model landing pages like:
- `/cars/bmw-x1`
- `/cars/bmw-x3`
- `/cars/bmw-x5`

unless no verified filtered inventory URL exists yet.

## Placement standard for comparison pages
Use the primary inventory CTA in three places when the page structure supports it:
1. top hero
2. middle verdict / decision section
3. bottom close / final CTA section

Primary CTA label pattern:
- `Shop X1 Inventory`
- `Shop X3 Inventory`
- `Shop X5 Inventory`

## Verified Brian Harris BMW model links

### X1
`https://brianharrisbmw.com/inventory?filters=%7B%22sortBy%22:%7B%22option%22:%7B%22label%22:%22Age%22,%22value%22:%22age%22,%22type%22:%22value%22%7D,%22direction%22:%22desc%22%7D,%22appliedFilters%22:%7B%22car_condition%22:%7B%22value%22:null%7D,%22model%22:%7B%22value%22:%7B%22X1%22:true%7D%7D%7D%7D`

### X3
`https://brianharrisbmw.com/inventory?filters=%7B%22sortBy%22:%7B%22option%22:%7B%22label%22:%22Age%22,%22value%22:%22age%22,%22type%22:%22value%22%7D,%22direction%22:%22desc%22%7D,%22appliedFilters%22:%7B%22car_condition%22:%7B%22value%22:null%7D,%22model%22:%7B%22value%22:%7B%22X3%22:true%7D%7D%7D%7D`

### X5
`https://brianharrisbmw.com/inventory?filters=%7B%22sortBy%22:%7B%22option%22:%7B%22label%22:%22Age%22,%22value%22:%22age%22,%22type%22:%22value%22%7D,%22direction%22:%22desc%22%7D,%22appliedFilters%22:%7B%22car_condition%22:%7B%22value%22:null%7D,%22model%22:%7B%22value%22:%7B%22X5%22:true%7D%7D%7D%7D`

## Rollout note
This pattern is now applied to Brian Harris BMW X1 / X3 / X5 content pages updated in this repo.

For other dealerships, add the store-specific verified filtered inventory URLs before swapping links. Do not guess or synthesize those URLs.
