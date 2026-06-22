# Data Dictionary

## prospects_2026
- `player_id`: stable player identifier
- `player_name`: player display name
- `position`: basketball role or position
- `age`: age on draft night if available
- `height_in`: height in inches
- `wingspan_in`: wingspan in inches
- `prospect_value_manual`: placeholder analyst grade, 0–100
- `creation_score`: ability to create shots / offense
- `shooting_score`: shooting projection
- `defense_score`: defensive tools and production
- `size_score`: physical size relative to role
- `rim_score`: rim protection / interior defensive signal
- `ready_now_score`: immediate NBA readiness
- `upside_score`: long-term upside
- `avg_mock_pick`: average mock draft slot
- `mock_std`: dispersion across mocks

## draft_order_2026
- `pick_number`: pick number
- `current_owner`: team currently holding the pick
- `original_team`: team that originally owned the pick
- `via_trade`: whether the pick changed hands before draft night
- `trade_risk_prior`: analyst prior for draft-night trade risk

## team_needs_2026
Need scores are scaled 0–1 and represent team-specific demand for a player trait.
