# Import the pygame module (make sure it's installed: pip install pygame)
import pygame

def main():
	# Set some window constants
	WIDTH = 640
	HEIGHT = 400
	STEP = 32

	# Default pygame initalization
	pygame.init()

	# Load the assets
	apple = pygame.image.load("apple.png")
	snakeHead = pygame.image.load("head.png")
	snakeTail = pygame.image.load("tail.png")
	snakeBody = pygame.image.load("body.png")

	# Create the main game area
	screen = pygame.display.set_mode((WIDTH, HEIGHT))

	# Add a clock to control the speed of the game
	clock = pygame.time.Clock()

	# A bit of design
	pygame.display.set_icon(apple)
	pygame.display.set_caption("Snake")

	# Variable to control the main loop
	running = True

	# Store snake's position
	snakeX = [(WIDTH - 32) / 2, (WIDTH - 32) / 2 - 32, (WIDTH - 32) / 2 - 64]
	snakeY = [(HEIGHT - 32) / 2, (HEIGHT - 32) / 2, (HEIGHT - 32) / 2]
	snakeR = [0, 0, 0]

	# Set step variables for the snake (do not move by default)
	stepX = STEP
	stepY = 0

	# Main (infinite) loop
	while running:
		# Gets all events from the queue
		for event in pygame.event.get():
			# If we want to quit...
			if event.type == pygame.QUIT:
				# ...exit the main loop, and therefore close the window
				running = False
			# If a key is pressed
			if event.type == pygame.KEYDOWN:
				# Prevent diagonal movement
				stepX = 0
				stepY = 0

				# Check the four arrows and tell the snake to move
				if event.key == pygame.K_UP:
					stepY = -STEP
				elif event.key == pygame.K_DOWN:
					stepY = STEP
				elif event.key == pygame.K_LEFT:
					stepX = -STEP
				elif event.key == pygame.K_RIGHT:
					stepX = STEP

		# Erase the entire screen
		screen.fill((255, 255, 255))

		# Draw the snake on screen
		for i in range(len(snakeX), 0, -1):
			# If max, draw the tail
			if i == len(snakeX):
				# Rotate the snake tile
				sprite = pygame.transform.rotate(snakeTail, snakeR[i - 1])
				screen.blit(sprite, (snakeX[i - 1], snakeY[i - 1]))
			# If min, draw the head
			elif i == 1:
				sprite = pygame.transform.rotate(snakeHead, snakeR[i - 1])
				screen.blit(sprite, (snakeX[i - 1], snakeY[i - 1]))
			else:
				sprite = pygame.transform.rotate(snakeBody, snakeR[i - 1])
				screen.blit(sprite, (snakeX[i - 1], snakeY[i - 1]))

		# Full screen update
		pygame.display.flip()

		for i in range(len(snakeX) - 1, 0, -1):
			snakeX[i] = snakeX[i - 1]
			snakeY[i] = snakeY[i - 1]
			snakeR[i] = snakeR[i - 1]

		# Move the snake on the two axis
		snakeX[0] += stepX
		snakeY[0] += stepY

		# Ensure proper tiles rotation
		if stepX > 0:
			snakeR[0] = 0
		elif stepX < 0:
			snakeR[0] = 180

		if stepY > 0:
			snakeR[0] = 270
		elif stepY < 0:
			snakeR[0] = 90

		# Check if the snake is still on screen
		if snakeX[0] >= (WIDTH - 32) or snakeX[0] <= 0:
			stepX = 0
		if snakeY[0] >= (HEIGHT - 32) or snakeY[0] <= 0:
			stepY = 0

		# Set the speed to 5 FPS
		clock.tick(5)


# Run the main function only if this module is executed as the main script
if __name__ == "__main__":
	main()
