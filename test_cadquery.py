import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(20, 40)
    .extrude(10)
    .faces(">Z")
    .circle(2.5)
    .cutBlind(-5)
)

result.val().exportStep("output/test_part.step")

print("CadQuery test completed successfully!")
print("STEP file exported to: output/test_part.step")