DATE=`date`

draw:
	@make -C basic draw
	@make -C coord draw
	@make -C gsd draw
	@make -C sequoia draw
	@make -C web draw
	pandoc --metadata title="$(DATE)" -s diff.md -o _diff.html

clean:
	@make -C basic clean
	@make -C coord clean
	@make -C gsd clean
	@make -C sequoia clean
	@make -C web clean
