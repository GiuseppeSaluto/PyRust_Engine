/// Complex pricing calculation with business logic
/// 
/// # Arguments
/// * `base` - Base price value
/// * `factor` - Multiplication factor
/// 
/// # Returns
/// Calculated final price with applied discounts
pub fn complex_calculation(base: f64, factor: f64) -> f64 {
    // Base calculation
    let base_calc = base * factor;
    
    // Apply volume-based discount tiers
    let discount_rate = match base_calc {
        x if x > 10000.0 => 0.85,  // 15% discount for large orders
        x if x > 5000.0 => 0.90,   // 10% discount for medium orders
        x if x > 1000.0 => 0.95,   // 5% discount for small orders
        _ => 1.0,                  // No discount
    };
    
    // Round to 2 decimal places for currency
    (base_calc * discount_rate * 100.0).round() / 100.0
}
