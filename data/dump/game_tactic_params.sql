INSERT INTO game_tactic_params VALUES('FC26','build_up_style','Short Passing','Players come short to support the carrier instead of running forward; slow transition, keeps defensive shape longest.');
INSERT INTO game_tactic_params VALUES('FC26','build_up_style','Balanced','Mix of forward runs and coming short; steady transition into the in-possession shape.');
INSERT INTO game_tactic_params VALUES('FC26','build_up_style','Counter','Players run in behind as the team transitions quickly from defence to attack.');
INSERT INTO game_tactic_params VALUES('FC26','defensive_approach','Deep','Safety-first; defensive line drops deep, tracks opposition runs.');
INSERT INTO game_tactic_params VALUES('FC26','defensive_approach','Balanced','Flexible depth; adjusts line and run-tracking situationally.');
INSERT INTO game_tactic_params VALUES('FC26','defensive_approach','High','High line with situational pressure; does not track runs closely (offside-trap risk).');
INSERT INTO game_tactic_params VALUES('FC26','defensive_approach','Aggressive','Highest-risk: high line + immediate counter-press after losing the ball, offside traps.');
INSERT INTO game_tactic_params VALUES('FC26','line_height','numeric','0-100 slider; selectable range is constrained by the chosen defensive_approach.');
INSERT INTO game_tactic_params VALUES('FC26','tactic_code','string','Shareable code encoding formation + build-up + defensive approach + line height + 11 roles/focuses.');
