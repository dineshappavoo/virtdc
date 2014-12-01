/**
 * 
 */

/**
 * @author Rahul
 *
 */
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;

import com.db.libraryapp.UtilityClasses.ValidationMessage;

/**
 * Created with IntelliJ IDEA.
 * User: Rahul Nair
 */
public class MainPanel extends JPanel {
	private static final String PATH = "D:\\IDEs\\Github\\virtdc\\vmonere\\monitor_logs\\";
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private static String vmid;
	private static MemoryMonitoringGraph memoryChart;
	private static CPUMonitoringGraph cpuChart;
	private static IOMonitoringGraph ioChart;
	public JTextField vmIdTextField;
	public JButton submit;

	public MainPanel() {
		super(new BorderLayout());
		setPreferredSize(new java.awt.Dimension(1024, 700));
		JPanel labelPanel = new JPanel();
		labelPanel.setSize(200, 100);
		vmIdTextField = new JTextField(20);
		vmIdTextField.setSize(100, 20);
		vmIdTextField.setHorizontalAlignment(SwingConstants.CENTER);
		submit = new JButton("Submit");
		submit.setSize(100,20);
		submit.setHorizontalAlignment(SwingConstants.CENTER);
		//vmIdTextField.setBounds(210, 50, 60, 20);
		JLabel text = new JLabel("VM ID : ");
		text.setHorizontalAlignment(SwingConstants.CENTER);
		text.setForeground(Color.blue);
		text.setFont(new Font("Cambria", Font.BOLD, 20));
		labelPanel.add(text);
		labelPanel.add(vmIdTextField);
		labelPanel.add(submit);
		final JPanel panel = new JPanel();
		JPanel northPanel = new JPanel();
		try {
			getMemGraph("VM_Task_100");
			getCPUGraph("VM_Task_100");
			getIOGraph("VM_Task_100");
		} catch (FileNotFoundException e1) {
			e1.printStackTrace();
		}
		northPanel.add(memoryChart, BorderLayout.EAST);
		northPanel.add(cpuChart, BorderLayout.WEST);
		northPanel.setVisible(true);
		panel.add(northPanel, BorderLayout.NORTH);
		panel.add(ioChart, BorderLayout.SOUTH);
		panel.setPreferredSize(new java.awt.Dimension(1024, 600));
		panel.setVisible(false);

		submit.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				if ("".equals(vmIdTextField.getText()) ) {
					ValidationMessage.alertMessage("Please enter the VM Id");
					vmIdTextField.requestFocusInWindow();
				} else {
					try {
						vmid = vmIdTextField.getText();
						getMemGraph(vmid);
						getCPUGraph(vmid);
						getIOGraph(vmid);
						panel.setVisible(true);
						
					} catch (FileNotFoundException fe) {
						System.out.println(fe.getMessage());
						panel.setVisible(false);
						ValidationMessage.alertMessage("Log for VM-"+vmid+" does not exist!");
					} 
					catch (Exception ex) {
						System.out.println(ex.getMessage());
						ValidationMessage.alertMessage(ex.getMessage());
					}
				}
			}
		});


		add(labelPanel,BorderLayout.NORTH);
		add(panel,BorderLayout.SOUTH);
	}
	public static void getMemGraph(String args) throws FileNotFoundException  {
		vmid = args;
		FileInputStream in;
		in = new FileInputStream(PATH+vmid+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		
		memoryChart = new MemoryMonitoringGraph("VM Monitoring", "Memory"+"-"+vmid, vmid, br);
		//memoryChart.pack();
		//RefineryUtilities.centerFrameOnScreen(memoryChart);
		memoryChart.setVisible(true);
		memoryChart.start();

	}

	public static void getCPUGraph(String args) throws FileNotFoundException {
		vmid = args;
		FileInputStream in;
		in = new FileInputStream(PATH+vmid+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		cpuChart = new CPUMonitoringGraph("VM Monitoring", "CPU"+"-"+vmid, vmid, br);
		//cpuChart.pack();
		//RefineryUtilities.centerFrameOnScreen(cpuChart);
		cpuChart.setVisible(true);
		cpuChart.start();

	}

	public static void getIOGraph(String args) throws FileNotFoundException {
		vmid = args;
		FileInputStream in;
		in = new FileInputStream(PATH+vmid+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		ioChart = new IOMonitoringGraph("VM Monitoring", "IO"+"-"+vmid, vmid, br);
		//cpuChart.pack();
		//RefineryUtilities.centerFrameOnScreen(cpuChart);
		ioChart.setVisible(true);
		ioChart.start();
	}

	private static void startMonitoring() {
		JFrame frame = new JFrame("VM Monitoring Application");
		frame.add(new MainPanel(), BorderLayout.CENTER);
		frame.pack();
		frame.setVisible(true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			@Override
			public void run() {
				startMonitoring();
			}
		});

	}
	
	public void paintComponent(Graphics g) {
	    super.paintComponent(g); // first draw a clear/empty panel
	    // then draw using your custom logic.
	  }
}