from omni.kit.async_engine import run_coroutine 
from isaacsim.robot.manipulators.examples.franka import Franka 
from omni.isaac.core import World 
from isaacsim.core.api.objects import DynamicCuboid 
from isaacsim.robot.manipulators.examples.franka.controllers import PickPlaceController 
import numpy as np 
import asyncio 
 
async def setup_scene(): 
    global world, franka, fancy_cube, controller 
     
    # Create world FIRST 
    world = World() 
    world.scene.add_default_ground_plane() 
 
    # Initialize physics BEFORE robot 
    await world.initialize_simulation_context_async()  # Critical for physics 
 
    # Add robot and cube 
    existing = world.scene.get_object("franka") 
    if not existing: 
        franka = Franka(prim_path="/World/Fancy_Franka", name="franka") 
        world.scene.add(franka) 
    else: 
        print("Object 'franka' already exists in the scene.") 
 
    existing_cube = world.scene.get_object("fancy_cube") 
    if not existing_cube: 
        fancy_cube = DynamicCuboid( 
                prim_path="/World/random_cube", 
                name="fancy_cube", 
                position=np.array([0.3, 0.3, 0.3]), 
                scale=np.array([0.0515, 0.0515, 0.0515]), 
                color=np.array([0, 0, 1.0]), 
            ) 
        world.scene.add(fancy_cube) 
    else: 
        print("Object 'fancy_cube' already exists in the scene.")  
 
    # 5. Create controller  
    controller = PickPlaceController( 
        name="pick_place_controller", 
        gripper=franka.gripper, 
        robot_articulation=franka 
    ) 
 
def physics_step(step_size): 
    print("=== Physics step ===") 
    print(fancy_cube) 
    cube_position, _ = fancy_cube.get_world_pose() 
    goal_position = np.array([-0.3, -0.3, 0.0515 / 2.0]) 
    current_joint_positions = franka.get_joint_positions() 
    print("Current joints:", current_joint_positions) 
    actions = controller.forward( 
        picking_position=cube_position, 
        placing_position=goal_position, 
        current_joint_positions=current_joint_positions, 
    ) 
     
    print("Computed actions:", actions) 
    franka.apply_action(actions) 
    new_joint_positions = franka.get_joint_positions() 
    print("New joints:", new_joint_positions) 
    if controller.is_done(): 
        world.pause() 
        world.reset() 
 
async def run_simulation(): 
    await world.play_async() 
    world.initialize_physics() 
    franka.initialize() 
    world.add_physics_callback("sim_step", physics_step) 
 
 
    # Initialize gripper AFTER simulation starts 
    franka.gripper.set_joint_positions(franka.gripper.joint_opened_positions) 
    await asyncio.sleep(1)  # Allow gripper to settle 
 
async def main(): 
    await setup_scene()  # First setup scene/robot 
    print("set up scene") 
    await run_simulation()  # Then run simulation 
    print("run sim") 
    await asyncio.sleep(10)  # Keep simulation running 
 
run_coroutine(main())