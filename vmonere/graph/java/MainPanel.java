import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;


/**
 * Main Panel for displaying the input field for VMID and the monitoring graphs
 * @author Rahul
 */
public class MainPanel extends JPanel {
	private static final String DOMAIN_PATH = "/var/lib/virtdc/vmonere/monitor_logs/domain/";
	private static final String HOST_PATH = "/var/lib/virtdc/vmonere/monitor_logs/host/";
	private static final long serialVersionUID = 1L;
	private static String vmid;
	private static MemoryMonitoringGraph memoryChart;
	private static CPUMonitoringGraph cpuChart;
	private static IOMonitoringGraph ioChart;
	private static MemoryMonitoringGraph hostOneMemoryChart;
	private static CPUMonitoringGraph hostOneCpuChart;
	private static IOMonitoringGraph hostOneIoChart;
	private static MemoryMonitoringGraph hostTwoMemoryChart;
	private static CPUMonitoringGraph hostTwoCpuChart;
	private static IOMonitoringGraph hostTwoIoChart;
	private static MemoryMonitoringGraph hostThreeMemoryChart;
	private static CPUMonitoringGraph hostThreeCpuChart;
	private static IOMonitoringGraph hostThreeIoChart;
	private static MemoryMonitoringGraph hostFourMemoryChart;
	private static CPUMonitoringGraph hostFourCpuChart;
	private static IOMonitoringGraph hostFourIoChart;
	public JTextField vmIdTextField;
	public JButton submit;
	public JPanel vmPanel;
	public JPanel leftPanel;
	public JPanel rightPanel;

	public MainPanel() {
		super(new BorderLayout());
		setPreferredSize(new java.awt.Dimension(1024, 700));

		/*VM PANEL*/

		leftPanel = new JPanel();
		leftPanel.setPreferredSize(new java.awt.Dimension(700,700));
		JPanel labelPanel = new JPanel();
		vmIdTextField = new JTextField(20);
		vmIdTextField.setSize(100, 20);
		vmIdTextField.setHorizontalAlignment(SwingConstants.CENTER);
		submit = new JButton("Submit");
		submit.setSize(100,20);
		submit.setHorizontalAlignment(SwingConstants.CENTER);
		JLabel text = new JLabel("Domain ID : ");
		text.setHorizontalAlignment(SwingConstants.CENTER);
		text.setForeground(Color.black);
		text.setFont(new Font("Calibri", Font.BOLD, 20));
		labelPanel.setSize(new java.awt.Dimension(600, 30));
		labelPanel.add(text);
		labelPanel.add(vmIdTextField);
		labelPanel.add(submit);
		vmPanel = new JPanel();
		JPanel northPanel = new JPanel();
		try {
			getMemGraph(null, 100000);
			getCPUGraph(null);
			getIOGraph(null);
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		if(memoryChart!= null) 
		{
			northPanel.add(memoryChart, BorderLayout.NORTH);
		}
		if(cpuChart != null) 
		{
			northPanel.add(cpuChart, BorderLayout.CENTER);
		}
		northPanel.setVisible(true);

		if(ioChart != null) 
		{
			northPanel.add(ioChart, BorderLayout.SOUTH);
		}
		vmPanel.add(northPanel, BorderLayout.SOUTH);
		vmPanel.setVisible(false);

		submit.addActionListener(new ActionListener() {
			/**
			 * Action for resetting the graphs for the new VM ID provided in the textfield
			 */
			@Override
			public void actionPerformed(ActionEvent e) {
				if ("".equals(vmIdTextField.getText()) ) {
					ValidationMessage.alertMessage("Please enter the domain Id");
					vmIdTextField.requestFocusInWindow();
				} else {
					try {

						vmid = vmIdTextField.getText();
						((Container)((Container) getComponent(1)).getComponent(1)).removeAll();
						((Container)((Container) getComponent(1)).getComponent(1)).repaint();
						JPanel northPanel = new JPanel(new BorderLayout());
						northPanel.setSize(new java.awt.Dimension(600,500));
						getMemGraph(vmid, 100000);
						getCPUGraph(vmid);
						getIOGraph(vmid);
						northPanel.add(memoryChart, BorderLayout.NORTH);
						northPanel.add(cpuChart, BorderLayout.CENTER);
						northPanel.add(ioChart, BorderLayout.SOUTH);
						northPanel.setVisible(true);
						((Container)((Container) getComponent(1)).getComponent(1)).add(northPanel, BorderLayout.SOUTH);
						((Container)((Container) getComponent(1)).getComponent(1)).setVisible(true);
						((Container)((Container) getComponent(1)).getComponent(1)).validate();
					} catch (FileNotFoundException fe) {
						System.out.println(fe.getMessage());
						vmPanel.setVisible(false);
						ValidationMessage.alertMessage("Log for VM-"+vmid+" does not exist!");
					} 
					catch (Exception ex) {
						System.out.println(ex.getMessage());
						ValidationMessage.alertMessage(ex.getMessage());
					}
				}
			}
		});

		leftPanel.add(labelPanel,BorderLayout.NORTH);
		leftPanel.add(vmPanel,BorderLayout.SOUTH);

		/*HOST PANEL*/
		rightPanel = new JPanel();
		rightPanel.setPreferredSize(new java.awt.Dimension(650,700));
		JPanel hostLabelPanel = new JPanel();
		JLabel hostHeader = new JLabel("Host Monitor");
		hostHeader.setHorizontalAlignment(SwingConstants.CENTER);
		hostHeader.setForeground(Color.black);
		hostHeader.setFont(new Font("Calibri", Font.BOLD, 18));
		hostHeader.setSize(520,20);
		hostLabelPanel.setSize(520,20);
		hostLabelPanel.add(hostHeader, BorderLayout.NORTH);

		JPanel hostMonitorPanel = new JPanel();
		hostMonitorPanel.setLayout(new GridLayout(4,1));
		JPanel hostOnePanel = new JPanel();
		hostOnePanel.setSize(500, 200);
		try {
			getHostMemGraph("node1", 1, 33554440);
			getHostCPUGraph("node1", 1);
			getHostIOGraph("node1", 1);
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		if(hostOneMemoryChart!= null) 
		{
			hostOnePanel.add(hostOneMemoryChart, BorderLayout.EAST);
		}
		if(hostOneCpuChart != null) 
		{
			hostOnePanel.add(hostOneCpuChart, BorderLayout.WEST);
		}

		if(hostOneIoChart != null) 
		{
			hostOnePanel.add(hostOneIoChart, BorderLayout.CENTER);
		}
		hostOnePanel.setVisible(true);


		JPanel hostTwoPanel = new JPanel();
		hostTwoPanel.setSize(500, 200);
		try {
			getHostMemGraph("node2", 2, 33554440);
			getHostCPUGraph("node2", 2);
			getHostIOGraph("node2", 2);
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		if(hostTwoMemoryChart!= null) 
		{
			hostTwoPanel.add(hostTwoMemoryChart, BorderLayout.EAST);
		}
		if(hostTwoCpuChart != null) 
		{
			hostTwoPanel.add(hostTwoCpuChart, BorderLayout.CENTER);
		}

		if(hostTwoIoChart != null) 
		{
			hostTwoPanel.add(hostTwoIoChart, BorderLayout.WEST);
		}

		hostTwoPanel.setVisible(true);

		JPanel hostThreePanel = new JPanel();
		hostThreePanel.setSize(500, 200);
		try {
			getHostMemGraph("node3", 3, 33554440);
			getHostCPUGraph("node3", 3);
			getHostIOGraph("node3", 3);
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		if(hostThreeMemoryChart!= null) 
		{
			hostThreePanel.add(hostThreeMemoryChart, BorderLayout.EAST);
		}
		if(hostThreeCpuChart != null) 
		{
			hostThreePanel.add(hostThreeCpuChart, BorderLayout.CENTER);
		}

		if(hostThreeIoChart != null) 
		{
			hostThreePanel.add(hostThreeIoChart, BorderLayout.WEST);
		}

		hostThreePanel.setVisible(true);

		JPanel hostFourPanel = new JPanel();
		hostFourPanel.setSize(500, 200);
		try {
			getHostMemGraph("node4", 4, 33554440);
			getHostCPUGraph("node4", 4);
			getHostIOGraph("node4", 4);
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		if(hostFourMemoryChart!= null) 
		{
			hostFourPanel.add(hostFourMemoryChart, BorderLayout.EAST);
		}
		if(hostFourCpuChart != null) 
		{
			hostFourPanel.add(hostFourCpuChart, BorderLayout.CENTER);
		}

		if(hostFourIoChart != null) 
		{
			hostFourPanel.add(hostFourIoChart, BorderLayout.WEST);
		}

		hostFourPanel.setVisible(true);
		hostMonitorPanel.add(hostOnePanel);
		hostMonitorPanel.add(hostTwoPanel);
		hostMonitorPanel.add(hostThreePanel);
		hostMonitorPanel.add(hostFourPanel);
		hostMonitorPanel.setVisible(true);
		rightPanel.add(hostLabelPanel);
		rightPanel.add(hostMonitorPanel);
		add(rightPanel, BorderLayout.EAST);
		add(leftPanel, BorderLayout.WEST);
	}

	/**
	 * Execute monitoring graph for Memory
	 * @param args
	 * @throws IOException 
	 * @throws ParseException 
	 */
	public static void getMemGraph(String args, int maxRange) throws IOException, ParseException  {
		if(args==null) return;
		vmid = args;
		FileInputStream in;
		in = new FileInputStream(DOMAIN_PATH+vmid+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		Date currentDate = new Date();
		String currentLine;
		Date d1 = null;
		Date d2 = null;
		while((currentLine = br.readLine()) != null) {
			if(currentLine.trim().equals("")) continue;
			String[] currentValues = currentLine.split("\\|");
			String strCurrLineDate = currentValues[0].trim();
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
			String strCurrentDate = format.format(currentDate);
			d1 = format.parse(strCurrentDate);
			d2 = format.parse(strCurrLineDate);

			long diff = Math.abs(d2.getTime() - d1.getTime());
			long diffSeconds = diff / 1000;
			if (diffSeconds < 10) break;
		}
		memoryChart = new MemoryMonitoringGraph("VM Monitoring", vmid+"-"+"Memory", vmid, br, 400, 200, maxRange);
		memoryChart.setVisible(true);
		memoryChart.start();

	}

	/**
	 * Execute monitoring graph for CPU
	 * @param args
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public static void getCPUGraph(String args) throws IOException, ParseException {
		if(args==null) return;
		vmid = args;
		FileInputStream in;
		in = new FileInputStream(DOMAIN_PATH+vmid+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		Date currentDate = new Date();
		String currentLine;
		Date d1 = null;
		Date d2 = null;
		while((currentLine = br.readLine()) != null) {
			if(currentLine.trim().equals("")) continue;
			String[] currentValues = currentLine.split("\\|");
			String strCurrLineDate = currentValues[0].trim();
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
			String strCurrentDate = format.format(currentDate);
			d1 = format.parse(strCurrentDate);
			d2 = format.parse(strCurrLineDate);
			long diff = Math.abs(d2.getTime() - d1.getTime());

			long diffSeconds = diff / 1000;
			if (diffSeconds < 10) break;

		}
		cpuChart = new CPUMonitoringGraph("VM Monitoring", vmid+"-"+"CPU", vmid, br, 400, 200);
		cpuChart.setVisible(true);
		cpuChart.start();

	}

	/**
	 * Execute monitoring graph for IO
	 * @param args
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public static void getIOGraph(String args) throws IOException, ParseException {
		if(args==null) return;
		vmid = args;
		FileInputStream in;
		in = new FileInputStream(DOMAIN_PATH+vmid+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		Date currentDate = new Date();
		String currentLine;
		Date d1 = null;
		Date d2 = null;
		while((currentLine = br.readLine()) != null) {
			if(currentLine.trim().equals("")) continue;
			String[] currentValues = currentLine.split("\\|");
			String strCurrLineDate = currentValues[0].trim();
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
			String strCurrentDate = format.format(currentDate);
			d1 = format.parse(strCurrentDate);
			d2 = format.parse(strCurrLineDate);
			long diff = Math.abs(d2.getTime() - d1.getTime());

			long diffSeconds = diff / 1000;
			if (diffSeconds < 10) break;

		}
		ioChart = new IOMonitoringGraph("VM Monitoring", vmid+"-"+"IO", vmid, br, 400, 200);
		ioChart.setVisible(true);
		ioChart.start();
	}




	/**
	 * Execute monitoring graph for Memory
	 * @param args
	 * @throws IOException 
	 * @throws ParseException 
	 */
	public static void getHostMemGraph(String args, Integer hostNumber, int maxRange ) throws IOException, ParseException  {
		if(args==null) return;
		String hostId = args;
		FileInputStream in;
		in = new FileInputStream(HOST_PATH+hostId+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		Date currentDate = new Date();
		String currentLine;
		Date d1 = null;
		Date d2 = null;
		while((currentLine = br.readLine()) != null) {
			if(currentLine.trim().equals("")) continue;
			String[] currentValues = currentLine.split("\\|");
			String strCurrLineDate = currentValues[0].trim();
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
			String strCurrentDate = format.format(currentDate);
			d1 = format.parse(strCurrentDate);
			d2 = format.parse(strCurrLineDate);
			long diff = Math.abs(d2.getTime() - d1.getTime());

			long diffSeconds = diff / 1000;
			if (diffSeconds < 10) break;

		}
		switch(hostNumber) {
		case 1 : hostOneMemoryChart = new MemoryMonitoringGraph("", hostId+"-"+"Memory", hostId, br, 200, 150, maxRange);
		hostOneMemoryChart.setVisible(true);
		hostOneMemoryChart.start();
		break;
		case 2 : hostTwoMemoryChart = new MemoryMonitoringGraph("", hostId+"-"+"Memory", hostId, br, 200, 150, maxRange);
		hostTwoMemoryChart.setVisible(true);
		hostTwoMemoryChart.start();
		break;
		case 3 : hostThreeMemoryChart = new MemoryMonitoringGraph("", hostId+"-"+"Memory", hostId, br, 200, 150, maxRange);
		hostThreeMemoryChart.setVisible(true);
		hostThreeMemoryChart.start();
		break;
		case 4 : hostFourMemoryChart = new MemoryMonitoringGraph("", hostId+"-"+"Memory", hostId, br, 200, 150, maxRange);
		hostFourMemoryChart.setVisible(true);
		hostFourMemoryChart.start();
		break;
		}

	}

	/**
	 * Execute monitoring graph for CPU
	 * @param args
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public static void getHostCPUGraph(String args, Integer hostNumber) throws IOException, ParseException {
		if(args==null) return;
		String hostId = args;
		FileInputStream in;
		in = new FileInputStream(HOST_PATH+hostId+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		Date currentDate = new Date();
		String currentLine;
		Date d1 = null;
		Date d2 = null;
		while((currentLine = br.readLine()) != null) {
			if(currentLine.trim().equals("")) continue;
			String[] currentValues = currentLine.split("\\|");
			String strCurrLineDate = currentValues[0].trim();
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
			String strCurrentDate = format.format(currentDate);
			d1 = format.parse(strCurrentDate);
			d2 = format.parse(strCurrLineDate);
			long diff = Math.abs(d2.getTime() - d1.getTime());

			long diffSeconds = diff / 1000;
			if (diffSeconds < 10) break;

		}

		switch(hostNumber) {
		case 1 : hostOneCpuChart = new CPUMonitoringGraph("", hostId+"-"+"CPU", hostId, br, 200, 150);
		hostOneCpuChart.setVisible(true);
		hostOneCpuChart.start();
		break;
		case 2 : hostTwoCpuChart = new CPUMonitoringGraph("", hostId+"-"+"CPU", hostId, br, 200, 150);
		hostTwoCpuChart.setVisible(true);
		hostTwoCpuChart.start();
		break;
		case 3 : hostThreeCpuChart = new CPUMonitoringGraph("", hostId+"-"+"CPU", hostId, br, 200, 150);
		hostThreeCpuChart.setVisible(true);
		hostThreeCpuChart.start();
		break;
		case 4 : hostFourCpuChart = new CPUMonitoringGraph("", hostId+"-"+"CPU", hostId, br, 200, 150);
		hostFourCpuChart.setVisible(true);
		hostFourCpuChart.start();
		break;
		}

	}

	/**
	 * Execute monitoring graph for IO
	 * @param args
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public static void getHostIOGraph(String args, Integer hostNumber) throws IOException, ParseException {
		if(args==null) return;
		String hostId = args;
		FileInputStream in;
		in = new FileInputStream(HOST_PATH+hostId+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		Date currentDate = new Date();
		String currentLine;
		Date d1 = null;
		Date d2 = null;
		while((currentLine = br.readLine()) != null) {
			if(currentLine.trim().equals("")) continue;
			String[] currentValues = currentLine.split("\\|");
			String strCurrLineDate = currentValues[0].trim();
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
			String strCurrentDate = format.format(currentDate);
			d1 = format.parse(strCurrentDate);
			d2 = format.parse(strCurrLineDate);
			long diff = Math.abs(d2.getTime() - d1.getTime());

			long diffSeconds = diff / 1000;
			if (diffSeconds < 10) break;

		}


		switch(hostNumber) {
		case 1 : hostOneIoChart = new IOMonitoringGraph("", hostId+"-"+"IO", hostId, br, 200, 150);
		hostOneIoChart.setVisible(true);
		hostOneIoChart.start();
		break;
		case 2 : hostTwoIoChart = new IOMonitoringGraph("", hostId+"-"+"IO", hostId, br, 200, 150);
		hostTwoIoChart.setVisible(true);
		hostTwoIoChart.start();
		break;
		case 3 : hostThreeIoChart = new IOMonitoringGraph("", hostId+"-"+"IO", hostId, br, 200, 150);
		hostThreeIoChart.setVisible(true);
		hostThreeIoChart.start();
		break;
		case 4 : hostFourIoChart = new IOMonitoringGraph("", hostId+"-"+"IO", hostId, br, 200, 150);
		hostFourIoChart.setVisible(true);
		hostFourIoChart.start();
		break;
		}
	}

	/**
	 * Initialize Main panel for monitoring
	 */
	private static void startMonitoring() {

		JFrame frame = new JFrame("Monitor");
		frame.add(new MainPanel(), BorderLayout.CENTER);
		frame.pack();
		frame.setVisible(true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		frame.setSize(screenSize);
	}

	/**
	 * Main function
	 * @param args
	 */
	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			@Override
			public void run() {
				startMonitoring();
			}
		});
	}
}