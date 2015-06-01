
/*
 * The story is: There is a factory with two assembly lines.
 * The assembly lines share a gate.
 * The parallel sequences of two assembly lines are:
 * FRAME_A_IN ->(2s) GATE ->(1.3s) ASSEMBLE_A ->(3.2s) PRODUCT_A_OUT
 * FRAME_B_IN ->(1.5s) GATE ->(0.9s) ASSEMBLE_B ->(3.4s) PRODUCT_B_OUT
 * There are multiple of above processes executing simultaneously.
 * We expect any anomaly detection algorithm to learn the two sequences mixed together,
 * and still detect the following anomalies:
 * FRAME_A_IN -> GATE -> ASSEMBLE_B
 */

var eventsA = [];
var eventsB = [];

function nextEventFrameA(time_now) {
	// FRAME_A_IN -> GATE -> ASSEMBLE_A -> PRODUCT_A_OUT
	var delay = 2000 + Math.floor((Math.random() * 100));
	time_now = time_now + delay;
	eventsA.push({
		event: "FRAME_A_IN",
		time: time_now
    });
	delay = 1300 + Math.floor((Math.random() * 100));
	time_now = time_now + delay;
	eventsA.push({
		event: "GATE",
		time: time_now
    });
	delay = 3200 + Math.floor((Math.random() * 100));
	time_now = time_now + delay;
	eventsA.push({
		event: "PRODUCT_A_OUT",
		time: time_now
    });
	return time_now;
}

function nextEventFrameB(time_now) {
    // FRAME_B_IN ->(1.5s) GATE ->(0.9s) ASSEMBLE_B ->(3.4s) PRODUCT_B_OUT
	var delay = 1500 + Math.floor((Math.random() * 100));
	time_now = time_now + delay;
	eventsB.push({
		event: "FRAME_B_IN",
		time: time_now
    });
	delay = 900 + Math.floor((Math.random() * 100));
	time_now = time_now + delay;
	eventsB.push({
		event: "GATE",
		time: time_now
    });
	delay = 3400 + Math.floor((Math.random() * 100));
	time_now = time_now + delay;
	eventsB.push({
		event: "PRODUCT_B_OUT",
		time: time_now
    });
	return time_now;
}

var RUNNING_TIME = 10000000; // 10000 s
var time_now = 0;
while (time_now <= RUNNING_TIME) {
	time_now = nextEventFrameA(time_now);
}
time_now = 0;
while (time_now <= RUNNING_TIME) {
	time_now = nextEventFrameB(time_now);
}
